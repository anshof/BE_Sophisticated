from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import ProductTypes
from blueprints import admin_required, buyer_required, seller_required
from blueprints import db, app

bp_product_type = Blueprint('product_type', __name__)
api = Api(bp_product_type)


class ProductTypeList(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = ProductTypes.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProductTypes.response_field))

        return rows, 200


class ProductTypeResource(Resource):
    def __init__(self):
        pass

    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        data = parser.parse_args()

        product_type = ProductTypes(
            data['name'], hash_pass, data['status'], salt)
        db.session.add(product_type)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product_type)

        return marshal(product_type, ProductTypes.response_field), 200, {'Content-Type': 'application/json'}

    def get(self, id):
        qry = ProductTypes.query.get(id)
        if qry is not None:
            return marshal(qry, ProductTypes.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    @admin_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        data = parser.parse_args()

        qry = ProductTypes.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.username = data['name']

        db.session.commit()

        return marshal(qry, ProductTypes.response_field), 200

    @admin_required
    def delete(self, id):
        qry = ProductTypes.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


api.add_resource(ProductTypeList, '', '')
api.add_resource(ProductTypeResource, '', '/<id>')
