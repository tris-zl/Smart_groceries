import mysql.connector
from aifc import Error

import flask
from flask import request, Flask

app = Flask(__name__)


def create_connection():
    db = None
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="Tris",
            passwd="SdjolSLgiDY7bhbjvBjL",
            database="smart_groceries"
        )

    except Error as e:
        print(e)

    return db


@app.route('/')
def welcome_screen():
    return 'Welcome to Smart Groceries'


@app.route('/shopping_site')
def shopping_site():
    db = create_connection()
    return products(db)


def products(db):
    my_cursor = db.cursor()
    my_cursor.execute("SELECT * FROM")
    rows = my_cursor.fetchall()
    return flask.jsonify(rows)


@app.route('/shoppingcart')
def return_all_products():
    db = create_connection()
    my_cursor = db.cursor()

    my_cursor.execute("SELECT * FROM shoppingcart")
    all_products = my_cursor.fetchall()
    return flask.jsonify(all_products)


@app.route('/add_to_shoppingcart')
def get_added():
    db = create_connection()
    product = request.args.get("product_name")
    quantity = request.args.get("quantity")
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    return add_product(db, product, quantity, first_name, last_name)


def add_product(db, product, quantity, first_name, last_name):
    my_cursor = db.cursor()
    sql = "INSERT INTO shoppingcart(product, quantity, first_name, last_name) VALUES (%s,%s,%s,%s);"
    my_cursor.execute(sql, (product, quantity, first_name, last_name))
    db.commit()
    db.close()
    return "successfully added"


@app.route('/check_users')
def get_sign_in_user():
    db = create_connection()
    email = request.args.get("email")
    password = request.args.get("password")
    return check_user(db, email, password)


def check_user(db, email, password):
    my_cursor = db.cursor()
    sql = "SELECT * FROM users WHERE email=(%s) AND password=(%s);"
    my_cursor.execute(sql, (email, password,))
    checked_user = my_cursor.fetchone()
    db.close()
    return flask.jsonify(checked_user[0], checked_user[1]) if checked_user[0] and checked_user[1] else ""


@app.route('/add_users')
def get_sign_up_user():
    db = create_connection()
    first_name = request.args.get("name")
    last_name = request.args.get("last_name")
    email = request.args.get("email")
    password = request.args.get("password")
    check_mail = check_email(db, email)
    return add_user(db, first_name, last_name, email, password) if 0 in check_mail else "Invalid enter"


def add_user(db, first_name, last_name, email, password):
    my_cursor = db.cursor()
    sql = "INSERT INTO users(name, last_name, email, password) VALUES (%s,%s,%s,%s);"
    my_cursor.execute(sql, (first_name, last_name, email, password))
    db.commit()
    db.close()
    return "successfully added"


def check_email(db, email):
    my_cursor = db.cursor()
    sql = "SELECT EXISTS(SELECT * FROM users WHERE name=(%s));"
    my_cursor.execute(sql, (email,))
    checked_email = my_cursor.fetchone()
    return checked_email


# my_cursor.execute("CREATE DATABASE smart_groceries")
# my_cursor.execute("CREATE TABLE shopping_list (product_name VARCHAR(100), person_name VARCHAR(50), "
#                   "quantity smallint UNSIGNED)")
# db = create_connection()
# my_cursor = db.cursor()
# my_cursor.execute("ALTER TABLE users ADD name VARCHAR(50), ADD last_name VARCHAR(50), "
#                  "ADD email VARCHAR(50), ADD password VARCHAR(50)")


if __name__ == '__main__':
    app.run(host="localhost", debug=True)
