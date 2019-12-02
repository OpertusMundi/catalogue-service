from flask_sqlalchemy import SQLAlchemy

from catalogueapi.database import db

class Item(db.Model):
    __tablename__ = "items"

    item_id = db.Column('id', db.Text, primary_key=True)
    title = db.Column('title', db.Text, nullable=False, index=True)
    description = db.Column('description', db.Text,
                nullable=False, index=True)
    creator = db.Column('creator', db.Text, index=True)

    def __init__(self,data):
        self.item_id = data.get('item_id')
        self.title = data.get('title')
        self.description = data.get('description')
        self.creator = data.get('creator')
