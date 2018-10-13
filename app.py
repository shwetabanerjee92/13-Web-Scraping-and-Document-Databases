# import necessary libraries
from flask import Flask, render_template, jsonify, redirect, current_app
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask
app = Flask(__name__)

mongo = PyMongo(app)

# create index route
@app.route("/")
def index():
    mars_data = mongo.db.mars.find_one()
    if bool(mars_data):
        return render_template("index.html", mars_dict=mars_data)
    else:
        return current_app.send_static_file('index.html')

# create scrape route
@app.route("/scrape")
def scrape():

    mars_dict = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars_dict.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)