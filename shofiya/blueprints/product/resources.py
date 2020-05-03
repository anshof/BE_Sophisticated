import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Products
from blueprints.seller.model import Seler
from blueprints.product_type.model import ProductTypes

from blueprints import db, app
from sqlalchemy import desc
from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_product = Blueprint('product', __name__)
api = Api(bp_product)


class ProductPromo(Resource):
    def get(self):  # mengambil data yang memiliki promo discount
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('order_by', location='args',
                            help='invalid orderby value', choices=['price', 'discount'])

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        qry = Products.query.filter_by(promo=True)
        qry = qry.filter_by(status=True)
        qry = qry.order_by(desc(Products.created_at))
        if args['order_by'] is not None:
            if args['order_by'] == 'price':
                qry = qry.order_by(Products.price)
            elif args['order_by'] == 'discount':
                qry = qry.order_by(Products.discount)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProductTypes.response_field))

        return rows, 200


class ProductResource(Resource):
    def __init__(self):
        pass

    # @internal_required
    def get(self):
        qry = Products.query.get(id)
        if qry is not None:
            return marshal(qry, Products.response_field), 200
        return {'status': 'NOT_FOUND'}, 404
    # @internal_required

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('color', location='json')
        parser.add_argument('weight', location='json')
        parser.add_argument('size', location='json')
        parser.add_argument('stock', location='json')
        parser.add_argument('promo', type=bool, location='json')
        parser.add_argument('discount', type=int, location='json')
        parser.add_argument('product_type_id', location='json')
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry = Sellers.query.filter_by(client_id=claims["id"]).first()
        seller_id = qry.id

        product = Products(args['name'], args['price'], args['color'],
                           args['weight'], args['size'], args['stock'], args['promo'], args['discount'], args['product_type_id'], seller_id)
        db.session.add(product)
        db.session.commit()
        app.logger.debug('DEBUG: %s', product)

        return marshal(product, Products.response_field), 200, {'Content-Type': 'application/json'}

    def patch(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('price', location='json')
        parser.add_argument('color', location='json')
        parser.add_argument('weight', location='json')
        parser.add_argument('size', location='json')
        parser.add_argument('stock', location='json')
        parser.add_argument('promo', type=bool, location='json')
        parser.add_argument('discount', type=int, location='json')
        parser.add_argument('product_type_id', location='json')
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry_seller = Sellers.query.filter_by(client_id=claims['id'])
        seller_id = qrySeller.id
        qry_product = Products.query.filter_by(seller_id=seller_id).all()
        qry = qry_product.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.name = args['name']
        qry.price = args['price']
        qry.color = args['color']
        qry.weight = args['weight']
        qry.size = args['size']
        qry.stock = args['stock']
        qry.promo = args['promo']
        qry.discount = args['discount']
        qry.product_type_id = args['product_type_id']
        db.session.commit()

        return marshal(product, Products.response_field), 200

    def delete(self, id):
        claims = get_jwt_claims()
        qry_seller = Sellers.query.filter_by(client_id=claims['id'])
        seller_id = qrySeller.id
        qry_product = Products.query.filter_by(seller_id=seller_id).all()

        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


class ProductList(Resource):
    def __init__(self):
        pass

    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('name', location='args')
        parser.add_argument('size', location='args')
        parser.add_argument('price', location='args')
        parser.add_argument('color', location='args')

        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=(
            'name', 'size', 'color', 'price'))
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = ProductTypes.query

        if args['size'] is not None:
            qry = qry.filter_by(id=args['size'])

        if args['color'] is not None:
            qry = qry.filter_by(id=args['color'])

        if args['name'] is not None:
            qry = qry.filter_by(id=args['name'])

        if args['price'] is not None:
            qry = qry.filter_by(id=args['price'])

        if args['orderby'] is not None:
            if args['orderby'] == 'name':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.name))
                else:
                    qry = qry.order_by(Products.name)
            elif args['orderby'] == 'size':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.size))
                else:
                    qry = qry.order_by(Products.size)
            elif args['orderby'] == 'color':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.color))
                else:
                    qry = qry.order_by(Products.color)
            elif args['orderby'] == 'price':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.price))
                else:
                    qry = qry.order_by(Products.price)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProductTypes.response_field))

        return rows, 200


class ProductSearch(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("keyword", location="args")
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('order_by', location='args',
                            help='invalid orderby value', choices=['price', 'discount'])

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        if args['keyword'] is not None:
            product = Products.query.filter(
                Products.name.like("%"+args['keyword']+"%") |
                ProductsTypes.name.like("%"+args['keyword']+"%") |
                Products.size.like("%"+args['keyword']+"%") |
                Products.color.like("%"+args['keyword']+"%"))

        product = product.order_by(desc(Products.created_at))
        if args['order_by'] is not None:
            if args['order_by'] == 'price':
                product = product.order_by(Products.price)
            elif args['order_by'] == 'sold':
                product = product.order_by(desc(Products.sold))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProductTypes.response_field))

        return rows, 200


api.add_resource(ProductList, '', '')
api.add_resource(ProductResource, '/<id>')
api.add_resource(ProductPromo, '', '')
api.add_resource(ProductSearch, '', '')
