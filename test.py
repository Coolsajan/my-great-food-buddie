
from app.data_ingestion.tripadviser_puller import TripAdviserDataPull

pull = TripAdviserDataPull(foodPlace="White rabbit pokhara")

result =pull.initiate_tripadviser_data_pull()
print(result)

