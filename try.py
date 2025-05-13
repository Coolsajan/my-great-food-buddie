import os
import re

from app.data_ingestion.google_maps_puller import GoogleMapsDataPull
from app.data_ingestion.tripadviser_puller import TripAdviserDataPull ,TripAdviserDataPullConfig
from app.preprocessing import CleanAndSaveToChromaDBC
from app.retriver import load_retriver

# Get user input
foodPlace = input("At which cafe are you right now?: ").lower()
safe_foodPlace = re.sub(r"[^\w.-]", "_", foodPlace)
vector_path = os.path.join("data", "vector_store", safe_foodPlace)


cleaner_store=CleanAndSaveToChromaDBC()
google = TripAdviserDataPull(foodPlace=foodPlace)
id = google.get_tripadviser_link()
print(id)

rev=google.get_reviews(review_link=id)

os.makedirs(TripAdviserDataPullConfig().review_save_file_path ,exist_ok=True)
path=google.initiate_tripadviser_data_pull()
cleaner_store.initiate_clean_chromadb(foodPlace=foodPlace,filepath=vector_path)

print(rev)