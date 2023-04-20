from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'username': user.username}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt_required
def protected():
    current_user = get_jwt_identity()
    return {'user_id': current_user}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        abort(401, 'Invalid username or password')

    access_token = create_access_token(identity=user)
    return {'access_token': access_token}
