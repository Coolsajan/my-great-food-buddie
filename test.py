import os
import re

from app.data_ingestion.google_maps_puller import GoogleMapsDataPull
from app.data_ingestion.tripadviser_puller import TripAdviserDataPull
from app.preprocessing import CleanAndSaveToChromaDBC
from app.retriver import load_retriver

from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA


# Get user input
foodPlace = input("At which cafe are you right now?: ").lower()
safe_foodPlace = re.sub(r"[^\w.-]", "_", foodPlace)
vector_path = os.path.join("data", "vector_store", safe_foodPlace)

    # Data ingestion if vector store doesn't exist
if os.path.exists(vector_path):
    print(f"\n[INFO] Vector store already exists for {foodPlace}. Skipping data pull.")
else:
    print(f"\n[INFO] Pulling data for {foodPlace}...")
    
    

    tripa = TripAdviserDataPull(foodPlace=foodPlace)
    tripa_path = tripa.initiate_tripadviser_data_pull()

    """google = GoogleMapsDataPull(foodPlace=foodPlace)
    google_path = google.initiate_google_maps_data_pull()"""

    cleaner_store = CleanAndSaveToChromaDBC()
    cleaner_store.initiate_clean_chromadb(foodPlace=foodPlace, filepath=[tripa_path])


# Load retriever
print("\n[INFO] Loading retriever and querying...")
retriever = load_retriver(foodPlace=foodPlace)

# Define prompt
prompt = ChatPromptTemplate.from_template("""
    You're a review analyst for a food company. Stay focused on the context and answer as clearly and naturally as possible.
    Think step by step and give the best answer.
    <context>
    {context}
    <context>
    Question: {question}
""")

# Load LLaMA 3 via Ollama
model = OllamaLLM(model="llama3",base_url="http://localhost:11434")

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=model,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

# Ask a question
question = input("Ask anything related to cafe : ")
result = qa_chain.invoke(question)


print(f"\n[ANSWER] {result['result']}")
