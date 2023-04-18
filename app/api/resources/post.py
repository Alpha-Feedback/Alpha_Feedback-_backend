from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.models import Post, User
from .extensions import db

import os


class PostResource(Resource):
    @jwt_required()
    def get(self, post_id):
        post = Post.query.get(post_id)
        if post:
            return jsonify(post.serialize()), 200
        else:
            return jsonify({"error": "Post not found"}), 404
    
    @jwt_required()
    def get_all(self):
        posts = Post.query.all()
        return jsonify([post.serialize() for post in posts]), 200
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        data = request.form
        if not data.get("description") or not request.files.get("image"):
            return jsonify({"error": "Missing required information"}), 400
        file = request.files.get("image")
        filename = secure_filename(file.filename)
        file.save(os.path.join("app/static/uploads", filename))
        post = Post(description=data.get("description"), image=filename, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return jsonify(post.serialize()), 201

    @jwt_required()
    def put(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        if post.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401
        data = request.form
        if data.get("description"):
            post.description = data.get("description")
        if request.files.get("image"):
            file = request.files.get("image")
            filename = secure_filename(file.filename)
            file.save(os.path.join("app/static/uploads", filename))
            post.image = filename
        db.session.commit()
        return jsonify(post.serialize()), 200

    @jwt_required()
    def delete(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        if post.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401
        db.session.delete(post)
        db.session.commit()
        return "", 204
