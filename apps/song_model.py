from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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

'create song object working'
newsong = Songs(name='Fix You', artist= 'Coldplay', year='2005') 

print(newsong.toDict())

"""
song object not able to be commited to the db
db.session.add(newsong)
db.session.commit() 

s = Songs.query.get(1)
print(s.toDict())
"""