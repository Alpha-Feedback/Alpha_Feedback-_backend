<!-- install dependencies -->
pip install -r requirements.txt

<!-- run flask -->
flask run

<!-- .env file  -->

    SECRET_KEY: Secret key used by Flask for session management. This should be set to a secure value.
    DATABASE_URL: URL for your database. If you are using MySQL, this will be in the format mysql://username:password@hostname/database.
    JWT_SECRET_KEY: Secret key used to sign JWT tokens for authentication. Make sure to set this to a secure value.
    REDIS_URL: URL for your Redis server if you are using it for rate limiting. If not, you can omit this.