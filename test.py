import os
import re

from data_ingestion.google_maps_puller import GoogleMapsDataPull
from data_ingestion.tripadviser_puller import TripAdviserDataPull
from app.preprocessing import CleanAndSaveToChromaDBC
from app.retriver import load_retriver

# Ask user for the cafe name
foodPlace = input("At which cafe are you right now?: ")

# Sanitize the input for use in file paths
safe_foodPlace = re.sub(r"[^\w.-]", "_", foodPlace)
vector_path = os.path.join("data", "vector_store", safe_foodPlace)

# If ChromaDB vector store already exists, proceed with pulling and cleaning data
if os.path.exists(vector_path):
    print(f"\n[INFO] Vector store already exists for {foodPlace}. Skipping data pull.")
else:
    print(f"\n[INFO] Pulling data for {foodPlace}...")

    tripa = TripAdviserDataPull(foodPlace=foodPlace)
    tripa_path = tripa.initiate_tripadviser_data_pull()

    google = GoogleMapsDataPull(foodPlace=foodPlace)
    google_path = google.initiate_google_maps_data_pull()

    file_path = [tripa_path, google_path]

    cleaner_store = CleanAndSaveToChromaDBC()
    cleaner_store.initiate_clean_chromadb(foodPlace=foodPlace, filepath=file_path)

# Load retriever and get results
print("\n[INFO] Loading retriever and querying...")
retriever = load_retriver(foodPlace=foodPlace)
results = retriever.invoke("What is the best food?")

# Display results
print("\n[RESULTS]")
for r in results:
    print(r.page_content)
    print("-" * 60)
