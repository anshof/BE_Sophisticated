import json
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Sellers
from blueprints.client.model import Clients
from blueprints import db, app
from sqlalchemy import desc
from blueprints import admin_required, seller_required, buyer_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_seller = Blueprint('seller', __name__)
api = Api(bp_seller)


class SellerResource(Resource):
    def __init__(self):
        pass

    def get(self, id):
        qry = Sellers.query.get(id)
        if qry is not None:
            return marshal(qry, Sellers.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    @seller_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('city', location='json', required=True)
        parser.add_argument('postal_code', location='json', required=True)
        parser.add_argument('city_type', location='json', required=True)
        parser.add_argument('street', location='json', required=True)
        parser.add_argument('phone', location='json')
        parser.add_argument('bank_account', location='json')

        args = parser.parse_args()

        seller = Sellers(args['name'], args['email'], args['province'], args['city'],
                         args['postal_code'], args['city_type'], args['street'], args['phone'], args['bank_account'])
        db.session.add(seller)
        db.session.commit()
        app.logger.debug('DEBUG: %s', seller)

        return marshal(seller, Sellers.response_field), 200, {'Content-Type': 'application/json'}

    @seller_required
    def patch(self, id):
        claims = get_jwt_claims()
        qry = Clients.query.get(claims['id'])
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
            parser = reqparse.RequestParser()
            parser.add_argument('name', location='json')
            parser.add_argument('email', location='json')
            parser.add_argument('province', location='json')
            parser.add_argument('city', location='json')
            parser.add_argument('postal_code', location='json')
            parser.add_argument('city_type', location='json')
            parser.add_argument('street', location='json')
            parser.add_argument('phone', location='json')
            parser.add_argument('bank_account', location='json')

            args = parser.parse_args()

            qry.name = args['name']
            qry.email = args['email']
            qry.province = args['province']
            qry.city = args['city']
            qry.postal_code = args['postal_code']
            qry.city_type = args['city_type']
            qry.street = args['street']
            qry.phone = args['phone']
            qry.bank_account = args['bank_account']

            db.session.commit()

            return marshal(seller, Sellers.response_field), 200, {'Content-Type': 'application/json'}


api.add_resource(SellerResource, '/profile', '/<id>')
