from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class PicProducts(db.Model):
    __tablename__ = "pic_product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),onupdate=func.now()) 
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    # products = db.relationship('Products', backref='product_type', lazy=True)   

    response_field = {
        'id': fields.Integer,
        'picture': fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime,
        'product_id':fields.Integer
    }

    def __init__(self, picture, product_id):
        self.picture = picture
        self.product_id = product_id
    
    def __repr__(self):
        return '<PicProduct %r>' % self.id