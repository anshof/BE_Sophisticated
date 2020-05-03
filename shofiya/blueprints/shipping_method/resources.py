from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import ShippingMethods
import hashlib
import uuid
from blueprints import internal_required
from blueprints import db, app

bp_shipping_method = Blueprint('shipping_method', __name__)
api = Api(bp_shipping_method)


class ShippingMethodList(Resource):
    def __init__(self):
        pass

    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = ShippingMethods.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ShippingMethods.response_field))

        return rows, 200


class ShippingMethodResource(Resource):
    def __init__(self):
        pass

    # admin only
    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courier', location='json', required=True)

        data = parser.parse_args()

        shipping_method = ShippingMethods(data['courier'])
        db.session.add(shipping_method)
        db.session.commit()

        app.logger.debug('DEBUG : %s', shipping_method)

        return marshal(shipping_method, ShippingMethods.response_field), 200, {'Content-Type': 'application/json'}

    # all
    # @internal_required
    def get(self, id):
        qry = ShippingMethods.query.get(id)
        if qry is not None:
            return marshal(qry, ShippingMethods.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    # admin only
    # @internal_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('courier', location='json')
        data = parser.parse_args()

        qry = ShippingMethods.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.courier = data['courier']
        qry.salt = salt

        db.session.commit()

        return marshal(qry, ShippingMethods.response_field), 200

    # admin only
    # @internal_required
    def delete(self, id):
        qry = ShippingMethods.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


api.add_resource(ShippingMethodList, '', '')
api.add_resource(ShippingMethodResource, '', '/<id>')
