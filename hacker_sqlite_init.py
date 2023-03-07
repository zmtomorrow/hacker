import sqlalchemy
print(sqlalchemy.__version__)

import sqlalchemy as db


engine = db.create_engine("sqlite:///hacker.sqlite")
connection = engine.connect()
metadata = db.MetaData()

story = db.Table('Story', metadata,
              db.Column('OfficalItemId', db.Integer(),primary_key=True),
              db.Column('title', db.String(255), nullable=False),
              db.Column('text', db.Text(), nullable=False),
              db.Column('url', db.String(255), nullable=False),
              db.Column('time', db.DateTime(), default=True)
              )

metadata.create_all(engine) 

