from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import cx_Oracle
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
api = Api(app)


sid = cx_Oracle.makedsn('host', 'port', service_name='service_name')
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://{user}:{password}@{sid}'.format(
    user='user',
    password='password!',
    sid=sid
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()

import views, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/login/access')
api.add_resource(resources.UserLogoutRefresh, '/login/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')



