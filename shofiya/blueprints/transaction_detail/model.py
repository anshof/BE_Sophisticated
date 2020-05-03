from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


class TransactionDetails(db.Model):
	__tablename__ = 'transaction_detail'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	transaction_id = dbColumn(db.Integer, db.ForeignKey('transaction.id'))
	product_id = dbColumn(db.Integer, db.ForeignKey('product.id'))
	price = db.Column(db.Integer, nullable=False)
	qty = db.Column(db.Integer, nullable=False)
	created_at = db.Column(db.DateTime(timezone=True),
	                       server_default=db.func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    product_review = db.relationship('ProductReviews', backref='transaction_detail', lazy=True)   

	response_field = {
		'id':fields.Integer,
		'transaction_id':fields.Integer,
		'product_id':fields.Integer,
		'price':fields.Integer,
		'qty':fields.Integer,
		'created_at': fields.DateTime,
		'updated_at': fields.DateTime
	}

	def __init__(self, transaction_id, product_id, price, qty):
		self.transaction_id = transaction_id
		self.product_id = product_id
		self.price = price
		self.qty = qty

	def __repr__(self):
		return '<TransactionDetail %r>' % self.id
