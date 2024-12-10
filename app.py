from flask import Flask, render_template, request, jsonify
import pandas as pd
from main import get_recommendations_with_details

from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the dataset
def load_data():
    data = pd.read_csv('dataset.csv')
    return data

# Prepare the data and encoder
data = load_data()
product_id_encoder = LabelEncoder()
product_id_encoder.fit(data['product_id'])

@app.route('/')
def home():
    # Get unique categories for dropdown
    categories = sorted(data['category'].unique())
    return render_template('index.html', categories=categories)

@app.route('/filter', methods=['POST'])
def filter_products():
    selected_category = request.form.get('category')
    filtered_data = data[data['category'] == selected_category]
    products = filtered_data[['product_id', 'product_name']].to_dict(orient='records')
    return jsonify(products)

@app.route('/details', methods=['POST'])
def product_details():
    product_name = request.form.get('product_name')
    selected_product = data[data['product_name'] == product_name].iloc[0]
    product_details = {
        "product_id": selected_product['product_id'],
        "product_name": selected_product['product_name'],
        "category": selected_product['category'],
        "rating": selected_product['rating'],
        "rating_count": selected_product['rating_count'],
        "img_link": selected_product['img_link'],
        "product_link": selected_product['product_link']
    }
    return jsonify(product_details)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    product_name = request.form.get('product_name')
    selected_product_id = data[data['product_name'] == product_name]['product_id'].values[0]
    product_id = product_id_encoder.transform([selected_product_id])[0]
    recommendations = get_recommendations_with_details(product_id=product_id)
    print(recommendations)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
