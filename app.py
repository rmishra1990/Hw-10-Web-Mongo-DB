from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from mars_scraping import *

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()
    print(mars_data)
    # destination_data['weather']
    # Return template and data
    return render_template("index.html", mars_data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    db=mongo.db.mars_data


    mars_data=main_mars_scrape_info()
    #database using update and upsert=True
    db.replace_one({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)







