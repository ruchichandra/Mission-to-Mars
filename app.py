# Dependencies
from flask import Flask, render_template, jsonify, redirect
import pymongo
from pymongo import MongoClient
from mLabCredentials import username, password
import scrape_mars

# Flask setup
app = Flask(__name__)

# client = MongoClient("mongodb://%s:%s@ds143245.mlab.com:43245/heroku_n5qzr3nx" % (username, password))
# client = MongoClient("mongodb://localhost:27017")

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
# db = client.heroku_n5qzr3nx

collection = db.mars

@app.route("/")
def index():
     mars_data = db.mars.find_one()
     return render_template("index.html", mars_data=mars_data)


@app.route('/scrape')
def scrape():
    mars = db.mars
    data = scrape_mars.scrape()

    print(data) 
    mars.update({}, data, upsert=True)

    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
# 