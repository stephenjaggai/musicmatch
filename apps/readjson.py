import cmd
import json
import sqlite3

with open ('songs.json', 'r') as f:
    jsondata = json.loads(f.read())


with sqlite3.connect("songs.db") as conn:
    keys = ["name", "artist"]
    for entry in jsondata:
        values = [entry.get(key, None) for key in keys]
        cmd = """INSERT INTO songs VALUES(
            ?,
            ?
            );"""
        conn.execute(cmd,values)  
    conn.commit()      