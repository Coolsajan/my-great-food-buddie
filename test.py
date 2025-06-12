from app.recommender import check_dB_data,retrieve_and_generate


foodPlace ="white rabbit pokhara"

Question = "Best food to try ?"



retriver = check_dB_data(foodPlace=foodPlace)
retrieve_and_generate(retriever=retriver , question=Question)