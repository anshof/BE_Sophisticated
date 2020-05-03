import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Transactions
from blueprints import db, app
from sqlalchemy import desc
from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.customer.model import Customers
from blueprints.product.model import Products

bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)


class TransactionResource(Resource):
    def __init__(self):
        pass

    # @internal_required
    # untuk buyer
    def get(self):
        claims = get_jwt_claims()
        qry = Transactions.query.get(claims['id'])
        if qry is not None:
            return marshal(qry, Transactions.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    # @jwt_required
    # @user_required
    def post(self):  # menambah produk ke keranjang user
        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=int, location="json")
        parser.add_argument("qty", type=int, location="json")
        args = parser.parse_args()

        claims = get_jwt_claims()
        customer_id = Customer.query.get(client_id)
        product = Products.query.get(args["product_id"])

        if product is None:
            return {"message": "Product Not Available"}, 404

        transaction = Transactions.query.filter_by(customer_id=customer_id)

        if transaction is None:
            transaction = Transactions(
                customer_id, payment_method_id, shipping_method_id)
            db.session.add(transaction)
            db.session.commit()

        transaction = transaction.filter_by(
            seller_id=product.seller_id).first()

        td = TransactionDetails(transaction.id,
                                args["product_id"], product.price, args["qty"])
        db.session.add(td)
        db.session.commit()

        transaction.total_qty += args["qty"]

        if product.promo:
            transaction.total_price += (int(product.price) *
                                        ((100-int(product.discount))/100)) * int(args['qty'])
        else:
            transaction.total_price += (int(product.price) * int(args["qty"]))

        transaction.updated_at = datetime.now()
        db.session.commit()

        return {'status': 'Success'}, 200


api.add_resource(TransactionResource, '/cart')
