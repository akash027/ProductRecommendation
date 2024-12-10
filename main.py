import requests
import logging
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the dataset
full_data = pd.read_csv('dataset.csv')

# Columns to drop for modeling purposes
columns_to_drop = [
    'product_name', 'category', 'discounted_price', 'actual_price',
    'discount_percentage', 'about_product', 'user_name', 'review_id',
    'review_title', 'review_content', 'img_link', 'product_link',
    'rating_count'
]

data = full_data.drop(columns=columns_to_drop)
data = data.dropna()
data = data[data.rating != '|']

# Label encoding
product_id_encoder = LabelEncoder()
user_id_encoder = LabelEncoder()
data['product_id'] = product_id_encoder.fit_transform(data['product_id'])
data['user_id'] = user_id_encoder.fit_transform(data['user_id'])

# API URL
API_URL = "https://2e94g9m5e9.execute-api.us-west-2.amazonaws.com/prodrec"

def fetch_recommendations(product_id):
    """
    Fetches product recommendations from the API for a given product_id.
    """
    try:
        logger.info(f"Fetching recommendations for product_id: {product_id}")
        # response = requests.post(API_URL, json={"product_id": product_id})
        response = requests.post(API_URL, json={"product_id": int(product_id)})

        if response.status_code == 200:
            recommendations = response.json().get("predictions", {}).get("predictions", [])
            logger.info(f"Received recommendations: {recommendations}")
            return recommendations
        else:
            logger.error(f"API call failed with status code {response.status_code}: {response.text}")
            return []
    except Exception as e:
        logger.error(f"Error fetching recommendations: {str(e)}")
        return []

def get_recommendations_with_details(product_id):
    """
    Fetches detailed product recommendations using the API.
    """
    recommended_ids = fetch_recommendations(product_id)
    if not recommended_ids:
        return []

    # Decode recommended IDs to original product IDs
    original_product_ids = product_id_encoder.inverse_transform(recommended_ids)

    recommendations = []
    for original_id in original_product_ids:
        try:
            product_details = full_data[full_data['product_id'] == original_id].iloc[0]
            recommendation_info = {
                'product_id': original_id,
                'product_name': product_details['product_name'],
                'category': product_details['category'],
                'rating': product_details['rating'],
                'rating_count': product_details['rating_count'],
                'img_link': product_details['img_link'],
                'product_link': product_details['product_link'],
            }
            recommendations.append(recommendation_info)
        except IndexError:
            logger.error(f"Product ID {original_id} not found in dataset.")
            continue
    print(recommendations)

    return recommendations
