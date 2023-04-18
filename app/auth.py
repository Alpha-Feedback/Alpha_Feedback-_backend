from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token

from .models import db, User

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'Missing email or password'}), 400

    email = data['email']
    password = generate_password_hash(data['password'])

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'msg': 'User already exists'}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    token = create_access_token(identity=new_user.id)

    return jsonify({'token': token}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'Missing email or password'}), 400

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'msg': 'Invalid email or password'}), 401

    token = create_access_token(identity=user.id)

    return jsonify({'token': token}), 200
