from flask import Flask, render_template
from pymongo import MongoClient
app = Flask(__name__)
mongodb_client = MongoClient("mongodb+srv://Lauren:qyDCpfewVq12UULK@cluster0.wviyb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongodb_client["shop_db"]
products_collection = db["products"]
mock_datat = [
    {"name": "child", "tag":"a real child. his name is Gabriel.", "price": 1000.00, "image_path": "/static/images/child.jpg"},
    {"name": "Balatro", "tag": "Balatro Steam key.", "price": 15.00, "image_path": "/static/images/balatro.jpg"},
    {"name": "Stardew Valley", "tag": "Stardew Valley Steam key.", "price": 10.00, "image_path": "/static/images/stardew_valley.jpg"},
    {"name": "Elden Ring", "tag": "Elden Ring Steam key.", "price": 50.00, "image_path": "/static/images/elden_ring.jpg"}
             ]
products_collection.insert_many(mock_datat)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    products = list(products_collection.find())
    return render_template("products.html", products=products)

app.run(host="0.0.0.0", port=5000)