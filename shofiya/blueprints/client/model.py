from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class Clients(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255 ))
    salt = db.Column(db.String(255))
    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),onupdate=func.now()) 
    customers = db.relationship('Customers', backref='client', lazy=True)   
    sellers = db.relationship('Sellers', backref='client', lazy=True)   
    
    response_field = {
        'id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'status':fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime
    }

    jwt_claim_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'status': fields.String
    }
    
    def __init__(self, username, password, status, salt):
        self.username = username
        self.password = password
        self.status = status
        self.salt = salt
    
    def __repr__(self):
        return '<Client %r>' % self.id