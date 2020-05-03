from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import ProductReviews
from blueprints.customer.model import Customers
from blueprints.transaction.model import Transactions
from blueprints.transaction_detail.model import TransactionDetails
from blueprints import internal_required
from blueprints import db, app

bp_product_review = Blueprint('product_review', __name__)
api = Api(bp_product_review)


class ProductReviewList(Resource):
    def __init__(self):
        pass

    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']

        qry = qry.order_by(desc(ProductReviews.created_at))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProductReviews.response_field))

        return rows, 200


class ProductReviewResource(Resource):
    def __init__(self):
        pass

    # buyer only
    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('picture', location='json')
        parser.add_argument('review', location='json', required=True)

        data = parser.parse_args()

        claims = get_jwt_claims()
        qry_customer = Customers.query.filter_by(
            client_id=claims['id']).first()
        customer_id = qry_customer.id
        qry_transaction = Transactions.query.filter_by(
            customer_id=customer_id).first()
        trans_id = qry_transaction.id
        qry_transdetail = TransactionDetails.query.filter_by(
            transaction_id=trans_id).first()
        transdetail_id qry_transdetail.id

        product_review = ProductReviews(
            data['picture'], data['review'], data['transaction_detail_id'])
        db.session.add(product_review)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product_review)

        return marshal(product_review, ProductReviews.response_field), 200, {'Content-Type': 'application/json'}

    # admin atau buyer
    # @internal_required
    def delete(self, id):
        qry = ProductReviews.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


api.add_resource(ProductReviewList, '', '')
api.add_resource(ProductReviewResource, '', '/<id>')
