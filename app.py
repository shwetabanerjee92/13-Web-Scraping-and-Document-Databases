# import necessary libraries
from flask import Flask, render_template, jsonify, redirect, current_app
from flask_pymongo import PyMongo
import mission_to_mars_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create index route
@app.route("/")
def index():
    marsdata = mongo.db.marsdata.find_one()
    return render_template("index.html", marsdata=marsdata)

@app.route("/scrape")
def scraper():
    mongo.db.marsdata.drop()
    results = mission_to_mars_scrape.scrape()
    mongo.db.marsdata.insert_one(results)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)