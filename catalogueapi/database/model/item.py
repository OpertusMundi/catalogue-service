import json
from flask_sqlalchemy import SQLAlchemy

from catalogueapi.database import db

class Item(db.Model):
    __tablename__ = "items"

    id = db.Column('id', db.Text, primary_key=True)

    title = db.Column('title', db.Text, nullable=False, index=True)
    description = db.Column('description', db.Text, index=True)
    creator = db.Column('creator', db.Text)
    item_json = db.Column('item_json', db.JSON)

    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.description = data.get('description')
        self.creator = data.get('creator')
        self.item_json = data
