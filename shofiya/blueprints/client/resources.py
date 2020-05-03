from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Clients

import hashlib, uuid
from blueprints import internal_required
from blueprints import db, app

bp_client = Blueprint('client', __name__)
api = Api(bp_client)


class ClientList(Resource):
    def __init__(self):
        pass
    
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('status', location='args', choices=('seller', 'buyer', 'admin'))
       
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']        
        qry = Clients.query
        
        if args['status'] is not None:
            qry = qry.filter_by(
                if args['status'] == 'seller': 
                    status='seller'
                elif args['status'] == 'buyer': 
                    status='buyer'
                else : 
                    status='admin'
                        )
                     
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Clients.response_field))
        
        return rows, 200
        
class ClientResource(Resource):
    def __init__(self):
        pass

    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('status', location='json', required=True,  choices=('seller', 'buyer', 'admin'))
        data = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (data['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()
        
        client = Clients(data['username'], hash_pass, data['status'], salt)
        db.session.add(client)
        db.session.commit()
        
        app.logger.debug('DEBUG : %s', client)
        
        return marshal(client, Clients.response_field), 200, {'Content-Type': 'application/json'}
 
    # @internal_required
    def get(self, id):
        qry = Clients.query.get( id)
        if qry is not None:
            return marshal(qry, Clients.response_field), 200
        return {'status':'NOT_FOUND'}, 404
 
    # @internal_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')
        data = parser.parse_args()

        qry = Clients.query.get(id)
        if qry is None:
            return {'status':'NOT_FOUND'}, 404

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (data['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        qry.username = data['username']
        qry.password = hash_pass
        qry.salt = salt
               
        db.session.commit()

        return marshal(qry, Clients.response_field), 200

    # @internal_required
    def delete(self, id):
        qry = Clients.query.get(id)
        if qry is None:
            return {'status':'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status':'DELETED'}, 200

api.add_resource(ClientList, '', '')
api.add_resource(ClientResource, '', '/<id>')