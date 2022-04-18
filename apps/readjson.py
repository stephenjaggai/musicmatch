import json
import sqlite3

db=sqlite3.connect('songs.db')
c=db.cursor()

openj =  json.load(open('songs.json'))
jdum = json.dumps(openj)
data = json.loads(jdum)


for record in data['tracks']:
    c.execute('INSERT INTO songs (name, artist) VALUES(?,?)',(record['name'],record['artist']))
    db.commit()

print('added successfully')


