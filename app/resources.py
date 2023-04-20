from flask import request
from flask_restful import Resource
from . import db, User, Issue, Sector, Upvote, Downvote
from marshmallow import Schema, fields, validate

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    school_id = fields.Integer(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return {'email': user.email, 'username': user.username, 'school_id': user.school_id, 'password': user.password}
            else:
                return {'message': 'User not found'}, 404
        else:
            users = User.query.all()
            result = []
            for user in users:
                result.append({'id': user.id, 'email': user.email, 'username': user.username, 'school_id': user.school_id, 'password': user.password})
            return result

    def post(self):
        email = request.json['email']
        username = request.json['username']
        school_id = request.json['school_id']
        password = request.json['password']
        user = User(email=email, username=username, school_id=school_id, password=password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created', 'data': {'id': user.id, 'email': user.email, 'username': user.username, 'school_id': user.school_id, 'password': user.password}}, 201
 
    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            email = request.json.get('email', user.email)
            username = request.json.get('username', user.username)
            school_id = request.json.get('school_id', user.school_id)
            password = request.json.get('password', user.password)
            user.email = email
            user.username = username
            user.school_id = school_id
            user.password = password
            db.session.commit()
            return {'message': 'User updated', 'id': user.id}
        else:
            return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted', 'id': user.id}
        else:
            return {'message': 'User not found'}, 404


class IssueResource(Resource):
    def get(self, issue_id=None):
        if issue_id:
            issue = Issue.query.get(issue_id)
            if issue:
                return {'description': issue.description, 'image_url': issue.image_url, 'upvotes': issue.upvotes, 'downvotes': issue.downvotes, 'user_id': issue.user_id, 'sector_id': issue.sector_id, 'status': issue.status, 'created_at': issue.created_at.isoformat(), 'updated_at': issue.updated_at.isoformat()}
            else:
                return {'message': 'Issue not found'}, 404
        else:
            issues = Issue.query.all()
            result = []
            for issue in issues:
                result.append({'id':issue.id,'description': issue.description, 'image_url': issue.image_url, 'upvotes': issue.upvotes, 'downvotes': issue.downvotes, 'user_id': issue.user_id, 'sector_id': issue.sector_id, 'status': issue.status, 'created_at': issue.created_at.isoformat(), 'updated_at': issue.updated_at.isoformat()})
            return result

    def post(self):
        description = request.json['description']
        image_url = request.json.get('image_url', '')
        upvotes = request.json.get('upvotes', 0)
        downvotes = request.json.get('downvotes', 0)
        user_id = request.json['user_id']
        sector_id = request.json['sector_id']
        status = request.json.get('status', 'open')
        issue = Issue(description=description, image_url=image_url, upvotes=upvotes, downvotes=downvotes, user_id=user_id, sector_id=sector_id, status=status)
        db.session.add(issue)
        db.session.commit()
        return {'message': 'Issue created', 'id': issue.id}, 201

    def put(self, issue_id):
        issue = Issue.query.get(issue_id)
        if issue:
            description = request.json.get('description', issue.description)
            image_url = request.json.get('image_url', issue.image_url)
            upvotes = request.json.get('upvotes', issue.upvotes)
            downvotes = request.json.get('downvotes', issue.downvotes)
            user_id = request.json.get('user_id', issue.user_id)
            sector_id = request.json.get('sector_id', issue.sector_id)
            status = request.json.get('status', issue.status)
            issue.description = description
            issue.image_url = image_url
            issue.upvotes = upvotes
            issue.downvotes = downvotes
            issue.user_id = user_id
            issue.sector_id = sector_id
            issue.status = status
            db.session.commit()
            return {'message': 'Issue updated', 'id': issue.id}
        else:
            return {'message': 'Issue not found'}, 404

    def delete(self, issue_id):
        issue = Issue.query.get(issue_id)
        if issue:
            db.session.delete(issue)
            db.session.commit()
            return {'message': 'Issue deleted', 'id': issue.id}
        else:
            return {'message': 'Issue not found'}, 404

class UpvoteResource(Resource):
    def post(self, issue_id, user_id):
        issue = Issue.query.filter_by(id=issue_id).first()
        user = User.query.filter_by(id=user_id).first()
        if issue and user:
            if user in issue.upvoters:
                return {"message": "User has already upvoted this issue"}, 400
            elif user in issue.downvoters:
                issue.downvotes -= 1
                issue.upvotes += 1
                issue.upvoters.append(user)
                issue.downvoters.remove(user)
            else:
                issue.upvotes += 1
                issue.upvoters.append(user)
            db.session.commit()
            return {"message": "Upvote successful"}, 200
        else:
            return {"message": "Issue or user not found"}, 404

class DownvoteResource(Resource):
    def post(self, issue_id, user_id):
        issue = Issue.query.filter_by(id=issue_id).first()
        user = User.query.filter_by(id=user_id).first()
        if issue and user:
            if user in issue.downvoters:
                return {"message": "User has already downvoted this issue"}, 400
            elif user in issue.upvoters:
                issue.downvotes += 1
                issue.upvotes -= 1
                issue.downvoters.append(user)
                issue.upvoters.remove(user)
            else:
                issue.downvotes += 1
                issue.downvoters.append(user)
            db.session.commit()
            return {"message": "Downvote successful"}, 200
        else:
            return {"message": "Issue or user not found"}, 404

class UpvotedIssuesResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": f"User with id {user_id} not found."}, 404

        upvoted_issues = Issue.query.join(Upvote).filter(Upvote.user_id == user_id).all()

        return {"upvoted_issues": [issue.id for issue in upvoted_issues]}

class DownvotedIssuesResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": f"User with id {user_id} not found."}, 404

        downvoted_issues = Issue.query.join(Downvote).filter(Downvote.user_id == user_id).all()

        return {"downvoted_issues": [issue.id for issue in downvoted_issues]}


class SectorResource(Resource):
    def get(self, sector_id=None):
        if sector_id:
            sector = Sector.query.get(sector_id)
            if sector:
                return {'name': sector.name}
            else:
                return {'message': 'Sector not found'}, 404
        else:
            sectors = Sector.query.all()
            result = []
            for sector in sectors:
                result.append({'id':sector.id,'name': sector.name})
            return result

    def post(self):
        name = request.json['name']
        sector = Sector(name=name)
        db.session.add(sector)
        db.session.commit()
        return {'message': 'Sector created', 'id': sector.id}, 201

    def put(self, sector_id):
        sector = Sector.query.get(sector_id)
        if sector:
            name = request.json.get('name', sector.name)
            sector.name = name
            db.session.commit()
            return {'message': 'Sector updated', 'id': sector.id}
        else:
            return {'message': 'Sector not found'}, 404

    def delete(self, sector_id):
        sector = Sector.query.get(sector_id)
        if sector:
            db.session.delete(sector)
            db.session.commit()
            return {'message': 'Sector deleted', 'id': sector.id}
        else:
            return {'message': 'Sector not found'}, 404



# from flask_restful import Resource, reqparse
# from flask import jsonify
# from .models import User, Issue, Sector, db

# user_parser = reqparse.RequestParser()
# user_parser.add_argument('email', type=str, help='Email address is required', required=True)
# user_parser.add_argument('username', type=str, help='Username is required', required=True)
# user_parser.add_argument('school_id', type=str, help='School ID is required', required=True)
# user_parser.add_argument('password', type=str, help='Password is required', required=True)

# issue_parser = reqparse.RequestParser()
# issue_parser.add_argument('description', type=str, help='Description is required', required=True)
# issue_parser.add_argument('image_url', type=str)
# issue_parser.add_argument('user_id', type=int, help='User ID is required', required=True)
# issue_parser.add
