import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Customers
from blueprints import db, app, admin_required, buyer_required, seller_required
from sqlalchemy import desc
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_customer = Blueprint('customer', __name__)
api = Api(bp_customer)


class CustomerResource(Resource):
    def __init__(self):
        pass

    @buyer_required
    @admin_required
    def get(self):
        claims = get_jwt_claims()
        qry = Customers.query.get(claims['id'])
        if qry is not None:
            return marshal(qry, Customers.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    @buyer_required
    def post(self):
        claims = get_jwt_claims()
        if claims['status'] == 'buyer':
            parser = reqparse.RequestParser()
            parser.add_argument('name', location='json', required=True)
            parser.add_argument('email', location='json', required=True)
            parser.add_argument('province', location='json', required=True)
            parser.add_argument('city', location='json', required=True)
            parser.add_argument('postal_code', location='json', required=True)
            parser.add_argument('city_type', location='json', required=True)
            parser.add_argument('street', location='json', required=True)
            parser.add_argument('phone', location='json')
            parser.add_argument('bod', location='json')
            parser.add_argument('client_id', location='json', default='show')

            args = parser.parse_args()

            customer = Customers(
                args['name'], args['email'], args['province'], args['city'], args['postal_code'], args['city_type'], args['street'], args['phone'], args['bod'], claims['id'])
            db.session.add(customer)
            db.session.commit()
            app.logger.debug('DEBUG: %s', customer)

            return marshal(customer, Customers.response_field), 200, {'Content-Type': 'application/json'}

    @buyer_required
    def patch(self, id):
        claims = get_jwt_claims()
        qry = Clients.query.get(claims['id'])
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('name', location='json')
            parser.add_argument('email', location='json')
            parser.add_argument('province', location='json')
            parser.add_argument('city', location='json')
            parser.add_argument('postal_code', location='json')
            parser.add_argument('city_type', location='json')
            parser.add_argument('street', location='json')
            parser.add_argument('phone', location='json')
            parser.add_argument('bod', location='json')

            args = parser.parse_args()

            qry.name = args['name']
            qry.email = args['email']
            qry.province = args['province']
            qry.city = args['city']
            qry.postal_code = args['postal_code']
            qry.city_type = args['city_type']
            qry.street = args['street']
            qry.phone = args['phone']
            qry.bod = args['bod']

            db.session.commit()

            return marshal(customer, Customers.response_field), 200


api.add_resource(CustomerResource, '/profile')
