from flask import Flask, render_template, request, abort
from hashlib import sha512

import db

app = Flask(__name__)
password_hash = b't\x9a#Bz\xc8n\xd9\xfa"I\x9d\xb9\xfatK\xcf\x8b\x83&\x1b[\xe5^\x83 \x88`&\xae\xfde\x985?"9\x87' \
                b'\xb5\xa3 2\\)\xdc\x08\xdb\xb3\xb2\x8bd\xd5\x17\xa4\xff\xb8\xca\x08\x0c\xe9\x16\x1f\x7f\x95'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db.add_recipe(request.form["username"],
                      request.form['recipe'],
                      False)
    search_query = request.args.get('q', "")
    return render_template('index.html',
                           admin=False,
                           search_query=search_query,
                           recipes=db.get_recipes(search_query))


@app.route('/admin/<password>', methods=['GET', 'POST'])
def admin(password):
    if not sha512(password.encode()).digest() == password_hash:
        abort(401, "You are not an admin!")
    if request.method == 'POST':
        db.add_recipe(request.form["username"],
                      request.form["recipe"],
                      request.form.get("hidden") == "on")
    search_query = request.args.get('q', "")
    return render_template('index.html',
                           admin=True,
                           search_query=search_query,
                           recipes=db.get_recipes(search_query, admin=True))
