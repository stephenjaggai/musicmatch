import json
import sqlite3

db=sqlite3.connect('songs.db')
c=db.cursor()

openj =  json.load(open('yt.json'))
jdum = json.dumps(openj)
data = json.loads(jdum)


for record in data['tracks']:
    c.execute('INSERT INTO youtube (name) VALUES(?)',(record['title'],))
    db.commit()

print('added successfully')

