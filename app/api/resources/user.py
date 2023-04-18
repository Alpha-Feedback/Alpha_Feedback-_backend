from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from .extensions import db


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.serialize()), 200
        else:
            return jsonify({"error": "User not found"}), 404

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"error": "Missing required information"}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 400
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 201
    
    @jwt_required()
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if username:
            user.username = username
        if password:
            user.password_hash = generate_password_hash(password)
        db.session.commit()
        return jsonify(user.serialize()), 200

    @jwt_required()
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return "", 204

    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        users = User.query.all()
        return jsonify([user.serialize() for user in users if user.id != current_user.id]), 200
