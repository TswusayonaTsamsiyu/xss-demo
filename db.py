import os
import sqlite3
import psycopg2

_IS_PROD = os.environ.get("mode", "dev") == "prod"
_DEV_DB = "recipes.db"
_PROD_DB = "postgres://ckzhgaznufpyio:65fe2044ba1f1e6b5fb93e83ebe43998ee4e1141a2e1a8d7533e83eab66bf94a@" \
           "ec2-34-255-225-151.eu-west-1.compute.amazonaws.com:5432/d7f123k4q62nts"

_INSERT_QUERY = 'INSERT INTO recipes (username, recipe, hidden) VALUES (?, ?, ?)'
if _IS_PROD:
    _INSERT_QUERY = _INSERT_QUERY.replace("?", "%s")


def connect_db():
    db = psycopg2.connect(_PROD_DB) if _IS_PROD else sqlite3.connect(_DEV_DB)
    db.cursor().execute('CREATE TABLE IF NOT EXISTS recipes '
                        f'(id {"SERIAL" if _IS_PROD else "INTEGER"} PRIMARY KEY, '
                        'username TEXT, '
                        'recipe TEXT, '
                        'hidden BOOL)')
    db.commit()
    return db


def add_recipe(username, recipe, hidden=False):
    db = connect_db()
    db.cursor().execute(_INSERT_QUERY, (username, recipe, hidden))
    db.commit()


def get_recipes(search_query, admin=False):
    query = f"""
    SELECT username, recipe
      FROM recipes
     WHERE ({admin} IS TRUE
            OR hidden IS FALSE)
       AND ('{search_query}' = ''
            OR UPPER (username) = UPPER ('{search_query}')
            OR recipe LIKE '%{search_query}%')
    """
    try:
        cursor = connect_db().cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as error:
        raise Exception(f"Failed to execute {query}") from error
