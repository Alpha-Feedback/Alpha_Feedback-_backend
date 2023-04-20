from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
# Models 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), nullable=False)
    school_id = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('issues', lazy=True))
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    sector = db.relationship('Sector', backref=db.backref('issues', lazy=True))
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    upvoters = db.relationship('User', secondary='upvote',
                               backref=db.backref('upvoted_issues', lazy=True))
    downvoters = db.relationship('User', secondary='downvote',
                                 backref=db.backref('downvoted_issues', lazy=True))


    def __repr__(self):
        return f'<Post {self.description,self.user_id }>'
class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)

class Downvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)

class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


def create_app():
    global app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///alphaFeedback1.db' or 'mysql://root:password@localhost/database'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'my-secret-key'
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    jwt = JWTManager(app)


    api = Api(app)
    db.init_app(app)


    # create db 
    with app.app_context():
        db.create_all()
        # db.create_all(app=app, models=[User, Issue, Sector])
    # populate_db()    # uncomment and run this only onces and comment back again



    # Import resources and routes 
    from .resources import HelloWorld, UserResource, IssueResource, SectorResource, UpvoteResource, DownvoteResource, UpvotedIssuesResource, DownvotedIssuesResource
    # from .routes import add_resources

    # Add resources to API 
    api.add_resource(HelloWorld, '/')
    api.add_resource(UserResource, '/users', '/users/<int:user_id>')
    api.add_resource(IssueResource, '/issues', '/issues/<int:issue_id>')
    api.add_resource(SectorResource, '/sectors', '/sectors/<int:sector_id>')
    api.add_resource(UpvoteResource, '/issues/<int:issue_id>/upvote/<int:user_id>')
    api.add_resource(DownvoteResource, '/issues/<int:issue_id>/downvote/<int:user_id>')
    api.add_resource(UpvotedIssuesResource, '/users/<int:user_id>/upvoted_issues')
    api.add_resource(DownvotedIssuesResource, '/users/<int:user_id>/downvoted_issues')

    

    return app

    
def populate_db():
    # db.session.query(Sector).delete()
    # db.session.commit()


    # Create first user
    user1 = User(email='user1@example.com', username='user1', school_id='123456', password='password1')
    # Create second user
    user2 = User(email='user2@example.com', username='user2', school_id='789012', password='password2')
    with app.app_context():
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()



    # Create Sector 
    # Define a list of sector names
    sector_names = ['Registrar', 'SITE', 'CBME', 'SECE', 'SMiE', 'SCBE', 'President Office','Student Service', 'Sport Dep', 'Campus Police']

    # Create a list of sector dictionaries
    sector_dicts = [{'name': name} for name in sector_names]

    # Create and commit new Sector instances for each dictionary
    with app.app_context():
        for sector_dict in sector_dicts:
            sector = Sector(**sector_dict)
            db.session.add(sector)
        db.session.commit()

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)