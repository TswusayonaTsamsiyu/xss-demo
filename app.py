from flask import Flask, render_template, request, abort

import db

app = Flask(__name__)
PASS = "brewster"


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
    if password != PASS:
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
