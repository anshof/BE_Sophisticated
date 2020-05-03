from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship


class ShippingMethods(db.Model):
    __tablename__ = "shipping_method"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courier = db.Column(db.String(30), nullable=False, unique=True)
    transactions = db.relationship(
        'Transactions', backref='shipping_method', lazy=True)

    response_field = {
        'id': fields.Integer,
        'courier': fields.String
    }

    def __init__(self, courier):
        self.courier = courier

    def __repr__(self):
        return '<ShippingMethod %r>' % self.id
