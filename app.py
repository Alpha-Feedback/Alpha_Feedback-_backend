from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)
api = Api(app)

# Define a model using SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Define a parser for handling request data
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name of the user')
parser.add_argument('email', type=str, help='Email of the user')

# Define a resource for handling GET and POST requests for users
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            users = User.query.all()
            return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])
        else:
            user = User.query.filter_by(id=user_id).first()
            if user is not None:
                return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
            else:
                return jsonify({'error': 'User not found'})

    def post(self):
        args = parser.parse_args()
        name = args['name']
        email = args['email']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

# Add the resource to the API
api.add_resource(UserResource, '/users', '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
