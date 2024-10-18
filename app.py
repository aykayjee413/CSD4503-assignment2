from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
mongodb_client = MongoClient(f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.wviyb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
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

app.run(host="0.0.0.0", port=5000)