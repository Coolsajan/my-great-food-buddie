import os
import traceback
from dotenv import load_dotenv

from app.data_ingestion.google_maps_puller import GoogleMapsDataPull
from app.data_ingestion.tripadviser_puller import TripAdviserDataPull
from app.preprocessing import CleanAndSaveToChromaDBC
from huggingface_hub import InferenceClient 

from app.retriver import load_retriver
from utils.common_utils import *
from langchain_huggingface import HuggingFaceEndpoint ,ChatHuggingFace ,HuggingFacePipeline
from langchain.prompts import ChatPromptTemplate ,PromptTemplate ,SystemMessagePromptTemplate,HumanMessagePromptTemplate
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA 


def check_dB_data(foodPlace):
    # Data ingestion if vector store doesn't exist
    vector_path = get_foodPlace_vector_path(foodPlace)
    if os.path.exists(vector_path):
        print(f"\n[INFO] Vector store already exists for {foodPlace}. Skipping data pull.")
    else:
        print(f"\n[INFO] Pulling data for {foodPlace}...")
        cleaner_store = CleanAndSaveToChromaDBC()
        
        try:
            tripa = TripAdviserDataPull(foodPlace=foodPlace)
            tripa_path = tripa.initiate_tripadviser_data_pull()
            cleaner_store.initiate_clean_chromadb(foodPlace=foodPlace, filepath=[tripa_path])
        except:
            print("No tripa data..")
            
        
        try:
            google = GoogleMapsDataPull(foodPlace=foodPlace)
            google_path = google.initiate_google_maps_data_pull()
            cleaner_store.initiate_clean_chromadb(foodPlace=foodPlace, filepath=[google_path])
        except:
            print("No data in google review....")

    # Load retriever
    print("\n[INFO] Loading retriever and querying...")
    retriever = load_retriver(foodPlace=foodPlace)
    print(retriever)
    for i , doc in enumerate(retriever,start=1):
        print(f"{i} : {doc.page_content}")
    return retriever

def retrieve_and_generate(retriever, question, use_hf=True):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "Use the following pieces of context to answer the question at the end. "
            "If you don't know the answer, just say you don't know — don't try to make up an answer."
        ),
        HumanMessagePromptTemplate.from_template(
            "Context:\n{context}\n\nQuestion:\n{question}\n\nHelpful Answer:"
        )
    ])

    try:
        if use_hf:
            load_dotenv(dotenv_path=".env")
            hf_token = os.getenv("NEW_HF_KEY")
            if not hf_token:
                raise EnvironmentError("Missing HUGGINGFACEHUB_API_TOKEN environment variable")

            llm = HuggingFaceEndpoint(
                repo_id="google/flan-t5-xl",
                temperature=0.7,
                huggingfacehub_api_token=hf_token,
                task="text2text-generation"
            )
        else:
            llm = OllamaLLM(model="llama2", temperature=0.7)

        print(f"Using model: {getattr(llm, 'repo_id', 'local model')}")

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )

        # Use 'query' key as per RetrievalQA interface
        result = qa_chain.invoke(question)

        return question, result["result"]

    except Exception as e:
        print(f"Generation Error: {e}")
        traceback.print_exc()
        return question, "Could not generate a response."
