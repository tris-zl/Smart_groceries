from db_smart_groceries import create_connection
import flask
from flask import request, Flask

app = Flask(__name__)


@app.route('/')
def welcome_screen():
    return 'Welcome to Smart Groceries'


# later for external api's
@app.route('/shopping_site')
def shopping_site():
    db = create_connection()
    return products(db)


def products(db):
    my_cursor = db.cursor()
    my_cursor.execute("SELECT * FROM")
    rows = my_cursor.fetchall()
    return flask.jsonify(rows)


@app.route('/new_group')
def get_group_attributes():
    db = create_connection()
    group_name = request.args.get("group_name")
    group_password = request.args.get("group_password")
    checked_team_name = check_team_name(db, group_name)
    return create_group(db, group_name, group_password)


def create_group(db, group_name, group_password):
    my_cursor = db.cursor()
    sql = "INSERT INTO teams(team_name, team_password) VALUES (%s,%s);"
    my_cursor.execute(sql, (group_name, group_password))
    db.commit()
    db.close()
    return "successfully added"


def check_team_name(db, group_name):
    my_cursor = db.cursor()
    sql = "SELECT EXISTS(SELECT * FROM teams WHERE team_name=(%s));"
    my_cursor.execute(sql, (group_name,))
    checked_group_name = my_cursor.fetchone()
    return checked_group_name[0] if checked_group_name == 0 else "Invalid enter. "


@app.route('/check_group_member')
def get_group_member():
    db = create_connection()
    group_name = request.args.get("group_name")
    group_password = request.args.get("group_password")
    return check_possible_member(db, group_name, group_password)


def check_possible_member(db, group_name, group_password):
    my_cursor = db.cursor()
    sql = "SELECT * FROM teams WHERE team_name=(%s) AND team_password=(%s);"
    my_cursor.execute(sql, (group_name, group_password))
    checked_member = my_cursor.fetchone()
    # return forename and last name
    return flask.jsonify(checked_member[0], checked_member[1])  # return group name and password


@app.route('/shoppingcart')
def return_all_products():
    db = create_connection()
    my_cursor = db.cursor()
    my_cursor.execute("SELECT * FROM shoppingcart")
    all_products = my_cursor.fetchall()
    return flask.jsonify(all_products)


# add product to shoppingcart
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


# check if users signin data already exists
@app.route('/check_users')
def get_sign_in_user():
    db = create_connection()
    email = request.args.get("email")
    password = request.args.get("password")
    return check_user(db, email, password)


def check_user(db, email, password):
    my_cursor = db.cursor()
    sql = "SELECT * FROM users WHERE email=(%s) AND password=(%s);"
    my_cursor.execute(sql, (email, password))
    checked_user = my_cursor.fetchone()
    # return forename and last name
    return flask.jsonify(checked_user[0], checked_user[1])


# add signup user to database
@app.route('/add_users')
def get_sign_up_user():
    db = create_connection()
    first_name = request.args.get("name")
    last_name = request.args.get("last_name")
    email = request.args.get("email")
    password = request.args.get("password")
    # check if typed in email exists already
    check_mail = check_email(db, email)
    return add_user(db, first_name, last_name, email, password) if check_mail == 0 else "Invalid enter. "


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
    return checked_email[0]


if __name__ == '__main__':
    app.run(host="localhost", debug=True)
