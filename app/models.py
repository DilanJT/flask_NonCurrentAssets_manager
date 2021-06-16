from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NonCurrentAsset(db.Model):
    __tablename__ = "noncurrentassets"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.toString(), nullable=False)
    assetType = db.Column(db.toString())
    assetValue = db.Column(db.Integer(), nullable=False)
    annualDepreciation = db.Column(db.Integer(), nullable=False)
    yearsUsed = db.Column(db.Integer(), nullable=False)
    netAmount = db.Column(db.Integer())
    totalDepreciation = db.Column(db.Integer())

    def __init__(self, id, name, assetType, assetValue, annualDepreciation, yearsUsed):
        self.id = id
        self.name = name
        self.assetType = assetType
        self.assetValue = assetValue
        self.annualDepreciation = annualDepreciation
        self.yearsUsed = yearsUsed
        self.totalDepreciation = self.annualDepreciation * self.yearsUsed
        self.netAmount = self.assetValue - self.totalDepreciation


    def __repr__(self):
        return f"{self.name}: AssetValue=Rs.{self.assetValue} | AnnualDepreciation=Rs.{self.annualDepreciation} | NetAmout=Rs.{self.netAmount}"