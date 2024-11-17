from http import client
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient, collection
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
mongodb_client = MongoClient("mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.wviyb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongodb_client["shop_db"]
products_collection = db["products"]
mock_datat = [
    {"name": "child", "tag":"a real child. his name is Gabriel.", "price": 999.99, "image_path": "/static/images/child.jpg"},
    {"name": "Balatro", "tag": "Balatro Steam key.", "price": 15.50, "image_path": "/static/images/balatro.jpg"},
    {"name": "Stardew Valley", "tag": "Stardew Valley Steam key.", "price": 10.50, "image_path": "/static/images/stardew_valley.jpg"},
    {"name": "Elden Ring", "tag": "Elden Ring Steam key.", "price": 50.50, "image_path": "/static/images/elden_ring.jpg"}
             ]
#products_collection.insert_many(mock_datat)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    products = list(products_collection.find())
    return render_template("products.html", products=products)

@app.route("/ping_db")
def ping_db():
    try:
        # Perform a simple ping to check the connection
        client.admin.command('ping')
        return "MongoDB connection is successful!"
    except Exception as e:
        return str(e), 500

@app.route("/add_product", methods=["POST"])
def add_product():
    product_data = request.get_json()
    result = collection.insert_one(product_data)
    if result.acknowledged:
        return jsonify({"status": "success"}), 201
    else:
        return jsonify({"status": "failure"}), 500

if __name__ == '__main__':
    app.run(debug=True)

app.run(host="0.0.0.0", port=5000)