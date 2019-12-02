import logging
from flask_sqlalchemy import SQLAlchemy

log = logging.getLogger(__name__)

db = SQLAlchemy()

def reset_database():
    db.drop_all()
    db.create_all()

def delete_database():
    db.drop_all()