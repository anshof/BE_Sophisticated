from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


class Products(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100))
    weight = db.Column(db.Integer, nullable=False)  # gram
    size = db.Column(db.String(10))
    stock = db.Column(db.Integer, nullable=False)
    promo = db.Column(db.Boolean, default=False)
    discount = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'))
    pic_products = db.relationship('PicProducts', backref='product', lazy=True)
    transaction_details = db.relationship(
        'TransactionDetails', backref='product', lazy=True)

    response_field = {
        'id': fields.Integer,
        'product_type_id': fields.Integer,
        'seller_id': fields.Integer,
        'name': fields.String,
        'price': fields.Integer,
        'color': fields.String,
        'weight': fields.Integer,
        'size': fields.String,
        'stock': fields.Integer,
        'promo': fields.Boolean,
        'discount': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    def __init__(self, name, price, color, weight, size, stock, promo, discount, product_type_id, seller_id):
        self.name = name
        self.price = price
        self.color = color
        self.weight = weight
        self.size = size
        self.stock = stock
        self.promo = promo
        self.discount = discount
        self.product_type_id = product_type_id
        self.seller_id = seller_id

    def __repr__(self):
        return '<Product %r>' % self.id
