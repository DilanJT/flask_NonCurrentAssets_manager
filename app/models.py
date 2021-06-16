from flask_sqlalchemy import SQLAlchemy

datab = SQLAlchemy()

class NonCurrentAsset(datab.Model):
    __tablename__ = "noncurrentassets"

    id = datab.Column(datab.Integer, primary_key=True)
    name = datab.Column(datab.String(), nullable=False)
    assetType = datab.Column(datab.String())
    assetValue = datab.Column(datab.Integer(), nullable=False)
    annualDepreciation = datab.Column(datab.Integer(), nullable=False)
    yearsUsed = datab.Column(datab.Integer(), nullable=False)
    netAmount = datab.Column(datab.Integer())
    totalDepreciation = datab.Column(datab.Integer())

    def __init__(self, name, assetType, assetValue, annualDepreciation, yearsUsed):
        self.name = name
        self.assetType = assetType
        self.assetValue = assetValue
        self.annualDepreciation = annualDepreciation
        self.yearsUsed = yearsUsed
        self.totalDepreciation = self.annualDepreciation * self.yearsUsed
        self.netAmount = self.assetValue - self.totalDepreciation


    def __repr__(self):
        return f"{self.name}: AssetValue=Rs.{self.assetValue} | AnnualDepreciation=Rs.{self.annualDepreciation} | NetAmout=Rs.{self.netAmount}"


