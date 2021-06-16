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

@app.route("/assets")
def readAssetsList():
    noncurrentassets = NonCurrentAsset.query.all()
    return render_template("assetlist.html", noncurrentassets=noncurrentassets)

@app.route('/assets/<int:id>')
def readAsset(id):
    asset = NonCurrentAsset.query.filter_by(id = id).first()
    if asset:
        return render_template('asset.html', asset = asset)
    return f"Cannot find the asset with id={id}"

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
            return redirect(f'/data/{id}')
        return f"Cannot find the asset with id={id}"
    return render_template("update.html", asset = asset)

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


app.run(host="localhost", port="5000")