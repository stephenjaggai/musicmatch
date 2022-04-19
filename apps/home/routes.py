# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from colorama import Cursor
from apps.home import blueprint
from flask import Flask, render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import pandas as pd

import sqlite3

app = Flask(__name__)
app.register_blueprint(blueprint)

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

import recsys.content_based_recsys
import ast

@blueprint.route('home/recsys_result')
def render_recsys_result():
    spotify_data = recsys.content_based_recsys.spotify_data
    username = request.args['username']
    playlist_id = request.args['playlist_id']
    tracks = recsys.content_based_recsys.get_playlist_tracks(username, playlist_id)
    ids = []
    for item in tracks:
        track = item['track']
        ids.append(track['id'])
    # loop over track ids to create dataset
    tracks = []
    for i in range(0, len(ids)):
        track = recsys.content_based_recsys.getTrackFeatures(ids[i])
        tracks.append(track)

    df = pd.DataFrame(tracks, columns = ['name', 'release_date'])
    df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d')
    df['year'] = pd.DatetimeIndex(df['release_date']).year
    df.drop(['release_date'], axis = 1, inplace = True)

    x = 0
    name = [0,1,2,3,4,5,6,7,8,9]
    year = [0,1,2,3,4,5,6,7,8,9]
    while x < 10:
        name[x] = str(df.at[x,'name'])
        name[x] = name[x].replace("'", "")
        name[x] = name[x].replace('"', "")
        year[x] = str(df.at[x,'year'])
        x = x + 1

    songs = "[{'name': '"+ name[0] + "', 'year': "+ year[0] +"}, \
    {'name': '"+ name[1] + "', 'year': "+ year[1] +"}, \
    {'name': '"+ name[2] + "', 'year': "+ year[2] +"}, \
    {'name': '"+ name[3] + "', 'year': "+ year[3] +"}, \
    {'name': '"+ name[4] + "', 'year': "+ year[4] +"}, \
    {'name': '"+ name[5] + "', 'year': "+ year[5] +"}, \
    {'name': '"+ name[6] + "', 'year': "+ year[6] +"}, \
    {'name': '"+ name[7] + "', 'year': "+ year[7] +"}, \
    {'name': '"+ name[8] + "', 'year': "+ year[8] +"}, \
    {'name': '"+ name[9] + "', 'year': "+ year[9] +"}]"
    
    songs = ast.literal_eval(songs)
    recommendations = recsys.content_based_recsys.recommend_songs(songs,spotify_data)
    recommendations = str(recommendations)
    return render_template('home/recsys_result.html', songs=songs, recommendations=recommendations)

@blueprint.route('/tables.html')
def render_catalog():
    headings = ("Songs","Artist")
    con = sqlite3.connect('songs.db')
    db = con.cursor()
    getsongs = db.execute('SELECT * FROM songs')
    return render_template('home/tables.html', data = getsongs.fetchall(), headings = headings)


@blueprint.route('/ytsongs.html')
def render_youtube():
    headings = ("Songs")
    con = sqlite3.connect('songs.db')
    db = con.cursor()
    getsongs = db.execute('SELECT * FROM youtube')
    return render_template('home/ytsongs.html', data = getsongs.fetchall(), headings = headings)


