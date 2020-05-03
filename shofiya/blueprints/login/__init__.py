from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from ..client.model import Clients
import hashlib
import uuid

bp_login = Blueprint('login', __name__)
api = Api(bp_login)


class CreateTokenResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        qry_client = Clients.query.filter_by(
            username=args['username']).first()

        if qry_client is not None:
            client_salt = qry_client.salt
            encoded = ('%s%s' %
                       (args['password'], client_salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            if hash_pass == qry_client.password and qry_client.username == args['username']:
                qry_client = marshal(qry_client, Users.jwt_client_fields)
                qry_client['identifier'] = "shofiya"
                token = create_access_token(
                    identity=args['username'], user_claims=qry_client)
                return {'token': token}, 200
        return {'status': 'UNAUTHORIZED', 'message': 'invalid username or password'}, 404


api.add_resource(CreateTokenResource, '')
