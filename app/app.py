from flask import Flask, render_template, request, redirect
from flask.signals import before_render_template
from models import db, NonCurrentAsset

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@before_render_template
def create_table():
    db.create_all()

@app.route("/assets/add", methods=['GET', "POST"])
def create():
    if request.method == "GET":
        return render_template("addasset.html")
    
    if request.method == "POST":

        # getting the values entered to the html form
        id = request.form["id"]
        name = request.form["name"]
        assetType = request.form["assetType"]
        assetValue = request.form["assetValue"]
        annualDepreciation = request.form["annualDepreciation"]
        yearsUsed = request.form["yearsUsed"]

        # adding to the database
        asset = NonCurrentAsset(id=id, name=name, assetType=assetType, assetValue=assetValue, annualDepreciation=annualDepreciation, yearsUsed=yearsUsed)
        db.session.add(asset)
        return redirect('/assets')

@app.route("/assets")
def readAssetsList():
    asset = NonCurrentAsset.query.all()
    return render_template("assetlist.html", asset=asset)

