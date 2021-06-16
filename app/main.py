from flask import Flask, render_template, request, redirect
from models import datab, NonCurrentAsset

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
datab.init_app(app)

@app.before_first_request
def create_table():
    datab.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/assets/add", methods=['GET', "POST"])
def create():
    if request.method == "GET":
        return render_template("addasset.html")
    
    if request.method == "POST":

        # getting the values entered to the html form
        name = request.form["name"]
        assetType = request.form["assetType"]
        assetValue = request.form["assetValue"]
        annualDepreciation = request.form["annualDepreciation"]
        yearsUsed = request.form["yearsUsed"]

        # adding to the database
        asset = NonCurrentAsset(name=name, assetType=assetType, assetValue=int(assetValue), annualDepreciation=int(annualDepreciation), yearsUsed=int(yearsUsed))
        datab.session.add(asset)
        datab.session.commit()
        return redirect('/assets')

@app.route("/assets")
def readAssetsList():
    noncurrentassets = NonCurrentAsset.query.all()
    return render_template("assetlist.html", noncurrentassets=noncurrentassets)


app.run(host="localhost", port="5000")