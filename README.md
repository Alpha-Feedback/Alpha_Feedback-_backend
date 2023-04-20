<!-- install dependencies -->
pip install -r requirements.txt

<!-- run flask -->
export FLASK_APP=run.py
export FLASK_ENV=development
flask run

<!-- .env file  -->

    SECRET_KEY: Secret key used by Flask for session management. This should be set to a secure value.
    DATABASE_URL: URL for your database. If you are using MySQL, this will be in the format mysql://username:password@hostname/database.
    JWT_SECRET_KEY: Secret key used to sign JWT tokens for authentication. Make sure to set this to a secure value.
  




