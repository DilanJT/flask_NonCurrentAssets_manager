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
    return redirect("/assets")

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

# read all the assets from the database
@app.route("/assets")
def readAssetsList():
    noncurrentassets = NonCurrentAsset.query.all()
    return render_template("assetlist.html", noncurrentassets=noncurrentassets)

# update a specific asset
@app.route('/assets/<int:id>/update', methods= ['GET', 'POST'])
def updateAsset(id):
    asset = NonCurrentAsset.query.filter_by(id = id).first()
    if request.method == 'POST':
        if asset:
            datab.session.delete(asset)
            datab.session.commit()
            name = request.form['name']
            assetType = request.form["assetType"]
            assetValue = request.form["assetValue"]
            annualDepreciation = request.form["annualDepreciation"]
            yearsUsed = request.form["yearsUsed"]

            asset = NonCurrentAsset(name=name, assetType=assetType, assetValue=int(assetValue), annualDepreciation=int(annualDepreciation), yearsUsed=int(yearsUsed))
            datab.session.add(asset)
            datab.session.commit()
            return redirect(f'/assets')
        return f"Cannot find the asset with id={id}"
    return render_template("updateasset.html", asset = asset)

@app.route('/assets/<int:id>/delete', methods=['GET', 'POST'])
def deleteAsset(id):
    asset = NonCurrentAsset.query.filter_by(id=id).first()
    if request.method == "GET":
        if asset:
            datab.session.delete(asset)
            datab.session.commit()
            print("deleted")
            return redirect('/assets')

    return redirect('/assets')


app.run(host="0.0.0.0", port="8080")