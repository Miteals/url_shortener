from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import string
import random
import os
from datetime import datetime, timedelta
from flask import jsonify


app = Flask(__name__)

url = "http://localhost:7778/"

log = []

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    ttl = db.Column(db.Integer, default=60)
    expiration_date = db.Column(db.DateTime)


my_model = MyModel(name='example', ttl=60)
db.session.add(my_model)
db.session.commit()

my_model = MyModel(name='example', ttl=60)
my_model.expiration_date = datetime.now() + timedelta(days=my_model.ttl)
db.session.add(my_model)
db.session.commit()

def retrieve_url(short_url):
    # retrieve the record from the database using the short_url
    url_record = MyModel.query.filter_by(short_url=short_url).first()
    if url_record is not None:
        if url_record.expiration_date > datetime.now():
            return jsonify({'url': url_record.long_url})
        else:
            db.session.delete(url_record)
            db.session.commit()
            return jsonify({'error': 'URL expired'}), 404
    else:
        return jsonify({'error': 'URL not found'}), 404

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=6)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(10))

    def __init__(self, long, short):
        self.long = long
        self.short = short

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url doesnt exist</h1>'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        url_received = request.form["url"]
        found_url = Urls.query.filter_by(long=url_received).first()

        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            print(short_url)
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template('index.html')


@app.route('/display/<url>', methods=['GET', 'POST'])
def display_short_url(url):
    return render_template('urlshort.html', short_url_display=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port =7778)