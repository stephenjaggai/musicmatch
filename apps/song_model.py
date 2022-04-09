import sqlite3
from flask import Flask, request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Songs(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    artist = db.Column('artist', db.String(50))
    year = db.Column('year', db.Integer)

    def toDict(self):
        return{
            'id' : self.id,
            'name' : self.name,
            'artist' : self.artist,
            'year' : self.year
        }

db.create_all()
'create song object working'
newsong = Songs(name='Ride', artist= '21 pilots', year='2015') 

'''print(newsong.toDict())'''




db.session.add(newsong)
db.session.commit() 




songs= Songs.query.all()

for song in songs:
    print (song.toDict())
