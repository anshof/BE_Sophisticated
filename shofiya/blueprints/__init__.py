from blueprints.client.resources import bp_client
from blueprints.customer.resources import bp_customer
from blueprints.login import bp_login
from blueprints.payment_method import bp_payment_method
from blueprints.pic_product.resources import bp_pic_product
from blueprints.product.resources import bp_product
from blueprints.product_review.resources import bp_product_review
from blueprints.product_type.resources import bp_product_type
from blueprints.seller.resources import bp_seller
from blueprints.shipping_method.resources import bp_shipping_method
from blueprints.transaction.resources import bp_transaction

import json
import config
import os
from functools import wraps
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims

app = Flask(__name__)

jwt = JWTManager(app)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] == 'admin':
            return {'status': 'FORBIDDEN', 'message': 'Admin Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def buyer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] == 'buyer':
            return {'status': 'FORBIDDEN', 'message': 'Buyer Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def seller_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] == 'seller':
            return {'status': 'FORBIDDEN', 'message': 'Seller Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


flask_env = os.environ.get('FLASK_ENV', 'Production')
if flask_env == 'Production':
    app.config.from_object(config.ProductionConfig)
elif flask_env == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))}))
    else:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))}))

    return response


app.register_blueprint(bp_client, url_prefix='/client')
app.register_blueprint(bp_customer, url_prefix='/customer')
app.register_blueprint(bp_login, url_prefix='/login')
app.register_blueprint(bp_payment_method, url_prefix='/payment_method')
app.register_blueprint(bp_pic_product, url_prefix='/pic_product')
app.register_blueprint(bp_product, url_prefix='/product')
app.register_blueprint(bp_product_review, url_prefix='/product_review')
app.register_blueprint(bp_product_type, url_prefix='/product_type')
app.register_blueprint(bp_seller, url_prefix='/seller')
app.register_blueprint(bp_shipping_method, url_prefix='/shipping_method')
app.register_blueprint(bp_transaction, url_prefix='/cart')

db.create_all()
