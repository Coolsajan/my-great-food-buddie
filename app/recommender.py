import os
import re

from app.data_ingestion.google_maps_puller import GoogleMapsDataPull
from app.data_ingestion.tripadviser_puller import TripAdviserDataPull
from app.preprocessing import CleanAndSaveToChromaDBC
from app.retriver import load_retriver
from utils.common_utils import *
from langchain import HuggingFaceHub
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
    return retriever

def retrive_generate(retriever,question):
    # Define prompt
    prompt = ChatPromptTemplate.from_template("""
        You're a review analyst for a food company. Stay focused on the context and answer as clearly and naturally as possible.
        Think step by step and give the best answer. And rember to give the humanly like result . and Just reply the answer dont use sentence like "as per ai"
        <context>
        {context}
        <context>
        Question: {question}
    """)

    # Load LLaMA 3 via Ollama
    #model = OllamaLLM(model="llama3",base_url="http://localhost:11434")
    hf = HuggingFaceHub(
    repo_id="meta-llama/Llama-2-7b-chat-hf",
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
)

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=hf,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    # Ask a question
    result = qa_chain.invoke(question)

    return result['query'] , result['result']



