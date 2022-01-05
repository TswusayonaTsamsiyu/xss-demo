import sqlite3


def connect_db():
    db = sqlite3.connect('recipes.db')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS recipes '
                        '(id INTEGER PRIMARY KEY, '
                        'username TEXT, '
                        'recipe TEXT, '
                        'hidden BOOL)')
    db.commit()
    return db


def add_recipe(username, recipe, hidden=False):
    db = connect_db()
    db.cursor().execute('INSERT INTO recipes (username, recipe, hidden) '
                        'VALUES (?, ?, ?)', (username, recipe, hidden))
    db.commit()


def get_recipes(search_query, admin=False):
    query = f"""
    SELECT username, recipe
      FROM recipes
     WHERE ({admin} IS TRUE
            OR hidden IS FALSE)
       AND ('{search_query}' IS NULL
            OR UPPER (username) = UPPER ('{search_query}')
            OR recipe LIKE '%{search_query}%')
    """
    return connect_db().cursor().execute(query).fetchall()
