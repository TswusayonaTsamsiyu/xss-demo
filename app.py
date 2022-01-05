from flask import Flask, render_template, request
import db

app = Flask(__name__)


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


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        db.add_recipe(request.form["username"],
                      request.form["recipe"],
                      request.form.get("hidden") == "on")
    search_query = request.args.get('q', "")
    return render_template('index.html',
                           admin=True,
                           search_query=search_query,
                           recipes=db.get_recipes(search_query, admin=True))
