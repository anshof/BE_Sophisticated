from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import PicProducts

import hashlib
import uuid
from blueprints import internal_required
from blueprints import db, app

bp_pic_product = Blueprint('pic_product', __name__)
api = Api(bp_pic_product)


class PicProductList(Resource):
    def __init__(self):
        pass

    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('product_id', location='args')
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = PicProducts.query.filter_by(id=args['product_id'])

        if args['sort'] == 'desc':
            qry = qry.order_by(desc(PicProducts.product_id))
        else:
            qry = qry.order_by(PicProducts.product_id)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, PicProducts.response_field))

        return rows, 200


class PicProductResource(Resource):
    def __init__(self):
        pass

    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('picture', location='json', required=True)
        parser.add_argument('product_id', location='json', required=True)

        data = parser.parse_args()

        qry_seller = Sellers.query.filter_by(client_id=claims["id"]).first()
        seller_id = qry_seller.id
        qry_product = Products.query.filter_by(seller_id=seller_id).all()
        qry_product_id = qry_product.filter_by(id=data["product_id"]).first()
        qry_pic = qry_product_id.id

        if qry_pic is None:
            return {'status': 'Belum ada produknya'}, 404

        pic_product = PicProducts(data['picture'], data['product_id'])
        db.session.add(pic_product)
        db.session.commit()

        app.logger.debug('DEBUG : %s', pic_product)

        return marshal(pic_product, PicProducts.response_field), 200, {'Content-Type': 'application/json'}

    # @internal_required
    def get(self, id):
        qry = PicProducts.query.get(id)
        if qry is not None:
            return marshal(qry, PicProducts.response_field), 200
        return {'status': 'NOT_FOUND'}, 404


api.add_resource(PicProductList, '', '')
api.add_resource(PicProductResource, '', '/<id>')
