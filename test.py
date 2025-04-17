from data_ingestion.google_maps_puller import GoogleMapsDataPull
from data_ingestion.tripadviser_puller import TripAdviserDataPull

foodPlace=input("At which cafe are u right now ...:")

tripa=TripAdviserDataPull(foodPlace=foodPlace)
tripa_path=tripa.initiate_tripadviser_data_pull()

google=GoogleMapsDataPull(foodPlace=foodPlace)
google_path=google.initiate_google_maps_data_pull()

print(tripa_path,google_path)