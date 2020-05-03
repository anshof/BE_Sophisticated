# import json, hashlib, uuid
# from flask import Blueprint
# from flask_restful import Api, Resource, marshal, reqparse, inputs
# from .model import TransactionDetails
# from blueprints import db, app
# from sqlalchemy import desc
# from blueprints import internal_required
# from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

# bp_transaction_detail = Blueprint('transaction_detail', __name__)
# api = Api(bp_transaction_detail)

# class TransactionDetailResource(Resource):
#     def __init__(self):
#         pass

#     # @internal_required
#     # untuk buyer
#     def get(self, id):
#         qry = TransactionDetails.query.get(id)
#         if qry is not None:
#             return marshal(qry, TransactionDetails.response_field), 200
#         return {'status':'NOT_FOUND'}, 404

#     # @internal_required
#     # untuk ke open api
#     def post(self):
#         claims = get_jwt_claims()
#         if claims['status']=='buyer':
#             parser = reqparse.RequestParser()
#             parser.add_argument('name', location='json', required=True)
#             parser.add_argument('email', location='json', required=True)
#             parser.add_argument('address', location='json')
#             parser.add_argument('phone', location='json')
#             parser.add_argument('bod', location='json')
#             parser.add_argument('client_id', location='json', default='show')

#             args = parser.parse_args()

#             transaction_detail = TransactionDetails(args['name'], args['email'], args['address'], args['phone'], args['bod'], claims['id'])
#             db.session.add(transaction_detail)
#             db.session.commit()
#             app.logger.debug('DEBUG: %s', transaction_detail)

#             return marshal(transaction_detail, TransactionDetails.response_field), 200, {'Content-Type': 'application/json'}

#  def patch(self, id):
#         claims = get_jwt_claims()
#         qry = Clients.query.get(claims['id'])
#         if qry is None:
#             return {'status':'NOT_FOUND'}, 404
#         else:
#             if claims['status']=='buyer':
#                 parser = reqparse.RequestParser()
#                 parser.add_argument('name', location='json')
#                 parser.add_argument('email', location='json')
#                 parser.add_argument('address', location='json')
#                 parser.add_argument('phone', location='json')
#                 parser.add_argument('bod', location='json')

#                 args = parser.parse_args()


#                 qry.name = args['name']
#                 qry.email = args['email']
#                 qry.address = args['address']
#                 qry.phone = args['phone']
#                 qry.bod = args['bod']

#                 db.session.commit()

#                 return marshal(transaction_detail, TransactionDetails.response_field), 200

# api.add_resource(TransactionDetailResource, '/me')
