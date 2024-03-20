#!/usr/bin/python3.10
# -*- coding: utf-8 -*-

import random
import json
import os

import Levenshtein

import anthropic

from flask import Flask
from flask import abort, render_template, request, jsonify, escape, redirect, url_for, send_file, session

app = Flask(__name__, static_folder='public', template_folder='views')

app.secret_key = os.environ.get('SECRET')

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line

def get_random_movie():  
    with open("filtered_movies.json", encoding="utf8") as my_file:
        movie_json = json.loads(random_line(my_file))
    title = movie_json["original_title"]
    pop = movie_json["popularity"]
    return [title,pop]

def get_emojis_from_movie(movie): # [string,int]
    client = anthropic.Anthropic() # defaults to os.environ.get("ANTHROPIC_API_KEY")
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.3,
        system="You are an AI that only returns emojis. You give the best represention of the movie requested by the user as emojis. You must only use the apropriate emojis that represents the movie. You must reference the plot, characters, title, and or movie beats as specific as possible.",
        messages=[
            {
                "role": "user",
                "content": movie
            }
        ]
    )
    return (message.content[0].text)

def get_movie_db_link(id):
    return f"https://www.themoviedb.org/movie/{id}"

@app.route('/debug')
def debug():
    if 'currEmoji' in session:
        session.pop('currEmoji')
    return ""
@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if request.method == "POST":
        guess = escape(request.args.get('guess', ''))
        session["guess"] = guess
        return redirect(url_for('guess'))
    
    if 'currEmoji' in session:
        title = session['currEmoji'][1]
    else:
        return redirect(url_for('index'))

    if 'guess' in session:
        guess = session['guess']
    else:
        return redirect(url_for('index'))
    print(Levenshtein.ratio(guess, title))
    return render_template('guess.html', title = title, correct = (Levenshtein.ratio(guess, title) > 0.65))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if 'currEmoji' in session:
            session.pop('currEmoji')
        if 'guess' in session:
            session.pop('guess')
        return redirect(url_for('index'))
    if 'currEmoji' in session:
        emojis = session['currEmoji'][0]
        title = session['currEmoji'][1]
    else:
        title = get_random_movie()[0]
        emojis = get_emojis_from_movie(title)
        session['currEmoji'] = [emojis,title]
    print(emojis)
    print(title)
    return render_template('index.html',emojis = emojis)

if __name__ == '__main__':
    app.run(debug=False)