from app import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

    # app.app_context().run(debug=True)
    # with app.app_context():
    #     app.run(debug=True)
