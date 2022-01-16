import os
import sqlite3
import psycopg2

_IS_PROD = os.environ.get("mode", "dev") == "prod"
_DEV_DB = "recipes.db"
_PROD_DB = "postgres://simodejyybtmpt:fb2c90e1245bcf6d18268e88255da8faafd3918a93fb0338a1c1fef12411faa2@" \
           "ec2-34-242-89-204.eu-west-1.compute.amazonaws.com:5432/dcjvpotkaofmhc"

_INSERT_QUERY = 'INSERT INTO recipes (username, recipe, hidden) VALUES (?, ?, ?)'
if _IS_PROD:
    _INSERT_QUERY = _INSERT_QUERY.replace("?", "%s")


def connect_db():
    db = psycopg2.connect(_PROD_DB, sslmode="require") if _IS_PROD else sqlite3.connect(_DEV_DB)
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


def get_recipes(query, admin=False):
    hidden_condition = "" if admin else "hidden IS FALSE"
    query_condition = f"UPPER (username) = UPPER ('{query}') OR recipe LIKE '%{query}%'" if query else ""
    conjoined = " AND ".join(f"({condition})" for condition in (hidden_condition, query_condition) if condition)
    final_cond = f"WHERE {conjoined}" if conjoined else ""
    query = f"SELECT username, recipe FROM recipes {final_cond}"
    print(query)
    try:
        cursor = connect_db().cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as error:
        raise Exception(f"Failed to execute {query}") from error
