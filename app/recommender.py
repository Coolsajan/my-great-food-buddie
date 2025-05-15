import os
import re

from app.data_ingestion.google_maps_puller import GoogleMapsDataPull
from app.data_ingestion.tripadviser_puller import TripAdviserDataPull
from app.preprocessing import CleanAndSaveToChromaDBC
from huggingface_hub import InferenceClient 

from app.retriver import load_retriver
from utils.common_utils import *
from langchain_huggingface import HuggingFaceEndpoint ,ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
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
    return retriever

def retrive_generate(retriever, question):
    # Use proper chat template
    prompt = ChatPromptTemplate.from_template("""
        [INST] <<SYS>>
        You're a food review analyst. Answer naturally using the context.
        <</SYS>>
        
        Context: {context}
        Question: {question} [/INST]
    """)

    # Configure HuggingFace Endpoint properly
    llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-2-7b",
    temperature=0.7,
    max_new_tokens=512,
    return_full_text=False,  # Moved out of model_kwargs
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    task="text-generation",
)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True  
    )

    try:
        result = qa_chain.invoke({"query": question})
        return question, result["result"]
    except Exception as e:
        print(f"Generation Error: {str(e)}")
        return question, "Could not generate response"    
