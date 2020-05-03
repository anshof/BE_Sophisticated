from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


class Transactions(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_price = db.Column(db.Integer, nullable=False)
    total_qty = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    payment_method = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    shipping_method = db.Column(db.Integer, db.ForeignKey('shipping_method.id'))
    transaction_detail = db.relationship(
        'TransactionDetails', backref='transaction', lazy=True)

    response_field = {
        'id': fields.Integer,
        'customer_id': fields.Integer,
        'payment_method_id': fields.Integer,
        'shipping_method_id': fields.Integer,
        'total_price': fields.Integer,
        'total_qty': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, customer_id, payment_method_id, shipping_method_id):
        self.customer_id = customer_id
        self.payment_method_id = payment_method_id
        self.shipping_method_id = shipping_method_id
        # self.total_price = total_price
        # self.total_qty = total_qty

    def __repr__(self):
        return '<Transaction %r>' % self.id
