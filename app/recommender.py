import os
import traceback
from dotenv import load_dotenv

from app.data_ingestion.google_maps_puller import GoogleMapsDataPull
from app.data_ingestion.tripadviser_puller import TripAdviserDataPull
from app.preprocessing import CleanAndSaveToChromaDBC
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory


from app.retriver import load_retriver 
from utils.common_utils import *
from langchain_huggingface import HuggingFaceEndpoint ,ChatHuggingFace ,HuggingFacePipeline
from langchain.prompts import ChatPromptTemplate ,PromptTemplate ,SystemMessagePromptTemplate,HumanMessagePromptTemplate
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain



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

    return retriever

def retrieve_and_generate(retriever, question, use_hf=True):
    prompt_template = """
    [INST]
    Your are an expert food review anylisis .Using the following contect reply the to the question as humally as possible .
    If you don't know the answer, say "I don't know.
    Start answer with "With deep analysis of reviews""

    Context:
    {context}

    Question:
    {question}
    [/INST]
    """

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )

    try:
        load_dotenv(dotenv_path=".env")
        hf_token = os.getenv("NEW_HF_KEY")
        if use_hf:
            if not hf_token:
                raise EnvironmentError("Missing HUGGINGFACEHUB_API_TOKEN environment variable")
            
            llm = HuggingFaceEndpoint(
                repo_id="mistralai/Mistral-7B-Instruct-v0.3",
                task="text-generation",
                huggingfacehub_api_token=hf_token,
                temperature=0.7,
                max_new_tokens=512
            )
        else:
            from langchain_ollama import OllamaLLM
            llm = OllamaLLM(model="llama2", temperature=0.5)

        docs = retriever.invoke(question)
        


        # Combine docs into context string
        context_text = "\n\n".join([doc.page_content for doc in docs])

        formatted_prompt = prompt.format(context=context_text, question=question)

        # Call LLM with a string prompt, NOT a dict
        response = llm.invoke(formatted_prompt)

        answer = response.strip()

        # Print retrieved docs for debugging
        print("\n--- Retrieved Documents ---")
        for i, doc in enumerate(docs):
            print(f"Doc {i+1}:\n{doc.page_content}\n")

        return question, answer

    except Exception as e:
        print(f"Generation Error: {e}")
        traceback.print_exc()
        return question, "Could not generate a response."