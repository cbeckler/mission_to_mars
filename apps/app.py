from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import apps.scraping as scraping

# set up flasl
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
## app.config is specifying connection to mongo using a URI
## the localhost is the url used to connect app to mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# setting up route for main html page users will see
@app.route("/")
def index():
    # find mars collection in mongo db (created by the scraping)
   mars = mongo.db.mars.find_one()
   # tells flask to build page based on index.html, using mars data
   return render_template("index.html", mars=mars)

# set up scraping route
@app.route("/scrape")
def scrape():
    # point to mars mongo db
   mars = mongo.db.mars
   # use scraping scipt to get data and store in var
   mars_data = scraping.scrape_all()
   # update db
   ## {} can contain query parameters (ex {"news_title": "Mars Landing Successful"} which would update where title matched). 
   ###      left {} it will update first matching doc in collection
   ## $set to our db
   ## upsert will insert data but not if indentical data already exists
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   # redirect navigates page back to / (index) where we can see updated content
   return redirect('/', code=302)

# code to run app
if __name__ == "__main__":
   app.run()