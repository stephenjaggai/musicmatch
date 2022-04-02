# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import Flask, render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

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
    songs = request.args['songs']
    songs = ast.literal_eval(songs)
    recommendations = recsys.content_based_recsys.recommend_songs(songs,spotify_data)
    recommendations = str(recommendations)
    return render_template('home/recsys_result.html', songs=songs, recommendations=recommendations)
