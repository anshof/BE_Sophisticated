from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import PaymentMethods

import hashlib
import uuid
from blueprints import admin_required, buyer_required, seller_required
from blueprints import db, app

bp_payment_method = Blueprint('payment_method', __name__)
api = Api(bp_payment_method)


class PaymentMethodList(Resource):
    def __init__(self):
        pass

    @buyer_required
    @admin_required
    @seller_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = PaymentMethods.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, PaymentMethods.response_field))

        return rows, 200


class PaymentMethodResource(Resource):
    def __init__(self):
        pass

    # just for admin
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        data = parser.parse_args()

        payment_method = PaymentMethods(data['name'])
        db.session.add(payment_method)
        db.session.commit()

        app.logger.debug('DEBUG : %s', payment_method)

        return marshal(payment_method, PaymentMethods.response_field), 200, {'Content-Type': 'application/json'}

    @buyer_required
    @admin_required
    @seller_required
    def get(self, id):
        qry = PaymentMethods.query.get(id)
        if qry is not None:
            return marshal(qry, PaymentMethods.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    # just for admin
    @admin_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        data = parser.parse_args()

        qry = PaymentMethods.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.username = data['name']

        db.session.commit()

        return marshal(qry, PaymentMethods.response_field), 200

    @admin_required
    def delete(self, id):
        qry = PaymentMethods.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


api.add_resource(PaymentMethodList, '', '')
api.add_resource(PaymentMethodResource, '', '/<id>')
