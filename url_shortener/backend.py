import secrets
from hashids import Hashids
import random
import string
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for

app = Flask(__name__)

database = []

hashids = Hashids(min_length=6, salt=app.config['SECRET_KEY'])

def generate_short_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

app.config.update(
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        short_url = request.form['short_url']

        database.append({"short_url": short_url})
    else:
        return jsonify(database)

app.run(host="0.0.0.0", port=7777)