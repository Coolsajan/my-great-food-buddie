import os,pickle,sys,re
from utils.logger import logging
from utils.exceptions import CustomException

def save_reviews(filepath,reviews):
    """This function will sall the list of data into file."""
    logging.info("saving reviews...")
    try:
        path=os.path.dirname(filepath)
        os.makedirs(path,exist_ok=True)
        with open(filepath,"wb") as f:
            pickle.dump(reviews,f)

    except Exception as e:
        raise CustomException(e,sys)
    
def load_reviews(filepath):
    """This function will load the reviews saved in selected filepath.."""
    logging.info("Loading reviews started...")
    try:
        with open(filepath,"rb") as f:
            reviews=pickle.load(f)

        return reviews
    except Exception as e:
        raise CustomException(e,sys)
        

def get_foodPlace_vector_path(foodPlace):
    try:
        safe_foodPlace = re.sub(r"[^\w.-]", "_", foodPlace)
        vector_path = os.path.join("tmp","data", "vector_store", safe_foodPlace)
    except Exception as e:
        raise CustomException(e,sys)
    
    return vector_path

food_recommendation_keywords = [
    # Taste & Flavor
    "delicious", "tasty", "flavorful", "bland", "undercooked", "spicy", "sweet",
    "salty", "sour", "overcooked", "authentic", "fresh", "dry", "greasy",

    # Recommendations & Popularity
    "best", "must try", "must-try", "recommended", "famous", "popular",
    "signature", "favorite", "specialty",

    # Dietary Restrictions / Preferences
    "vegan", "vegetarian", "gluten-free", "halal", "keto", "lactose-free", "healthy",

    # Portion / Value
    "portion", "serving", "size", "value", "worth", "expensive", "cheap", "affordable",
    "enough for two", "shareable", "good for sharing",

    # Ambience / Setting
    "romantic", "family-friendly", "quiet", "casual", "luxury", "cozy", "view", "ambience",

    # Service
    "friendly", "slow", "fast service", "attentive", "rude", "welcoming", "staff",

    # Meal Type / Time
    "breakfast", "brunch", "lunch", "dinner", "late night", "dessert", "snacks",

    # Cuisine Types
    "italian", "indian", "mexican", "thai", "japanese", "seafood", "bbq", "burger",
    "pizza", "noodles", "steak", "pasta", "curry", "sushi",

    # Mood / Emotions
    "craving", "comfort food", "celebration", "feel like eating", "hungry", "something new"
]


def trig_retriver(question, keywords = food_recommendation_keywords):
    question_key = list(question.split())

    for keys in question_key:
        if keys in keywords:
            retiver = True
        else :
            retriver = False
    return retriver

def clean_markdown(text):
    return re.sub(r"```[\s\S]*?```", lambda m: m.group(0).strip('`').strip(), text)

