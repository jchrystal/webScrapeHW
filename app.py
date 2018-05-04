from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db


@app.route("/")
def index():
    listings = list(db.listings_mars.find())
    print(listings)
    return render_template("index.html", listings=listings)

@app.route("/scrape")
def scrape():
    listings = db.listings_mars
    mars_dict = scrape_mars.scrape()
    listings.drop()
    listings.insert_one(mars_dict)
    #listings.update({"newsTitle": mars_dict['newsTitle'], "newsParagraph": mars_dict['newsParagraph'], "featuredImage": mars_dict['featuredImage'], "marsWeather": mars_dict['marsWeather'], "marsData": mars_dict['marsData'], "marsHemispheres": mars_dict['marsHemispheres']}, mars_dict, upsert=True)
    return redirect("http://127.0.0.1:5000/", code=302)




if __name__ == "__main__":
    app.run(debug=True)