
def generate_db_schema(config_file=None):
    '''Generate database schema from ORM definitions'''

    from .app import create_app
    from .database import db

    app = create_app(config_file)
    with app.app_context():
        db.create_all()

