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
    user_id = request.args.get("user_id")
    group_name = request.args.get("group_name")
    group_password = request.args.get("group_password")
    return create_group(db, user_id, group_name, group_password)


def create_group(db, user_id, group_name, group_password):
    my_cursor = db.cursor()
    sql = "INSERT INTO teams(team_name, team_password) VALUES (%s,%s);"
    my_cursor.execute(sql, (group_name, group_password))
    db.commit()

    sql_2 = "SELECT * FROM teams WHERE team_name=(%s) AND team_password=(%s);"
    my_cursor.execute(sql_2, (group_name, group_password))
    checked_member = my_cursor.fetchone()

    sql_3 = "INSERT INTO teams_users(group_id, user_id) VALUES (%s,%s);"
    my_cursor.execute(sql_3, (checked_member[0], user_id))  # insert group_id and user_id into groups_users
    db.commit()
    db.close()
    return "successfully added"


@app.route('/join_team')
def get_group_member():
    db = create_connection()
    user_id = request.args.get("user_id")
    group_name = request.args.get("group_name")
    group_password = request.args.get("group_password")
    return add_to_team(db, user_id, group_name, group_password)


def add_to_team(db, user_id, group_name, group_password):
    my_cursor = db.cursor()
    sql = "SELECT * FROM teams WHERE team_name=(%s) AND team_password=(%s);"
    my_cursor.execute(sql, (group_name, group_password))
    checked_member = my_cursor.fetchone()

    sql_2 = "INSERT INTO teams_users(group_id, user_id) VALUES (%s,%s);"
    my_cursor.execute(sql_2, (checked_member[0], user_id))  # insert group_id and user_id into groups_users
    return "successfully added"


@app.route('/give_user_ids')
def get_data():
    db = create_connection()
    email = request.args.get("email")
    return get_user_id(db, email)


def get_user_id(db, email):
    my_cursor = db.cursor()
    sql = "SELECT * FROM users WHERE email=(%s);"
    my_cursor.execute(sql, (email,))
    checked_user = my_cursor.fetchone()
    # return user_id
    return flask.jsonify(checked_user[0])


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
    return check_user(db, email)


def check_user(db, email):
    my_cursor = db.cursor()
    sql = "SELECT * FROM users WHERE email=(%s);"
    my_cursor.execute(sql, (email,))
    checked_user = my_cursor.fetchone()
    # return forename and last name
    return flask.jsonify(checked_user[1], checked_user[2])


# add signup user to database
@app.route('/add_users')
def get_sign_up_user():
    db = create_connection()
    first_name = request.args.get("name")
    last_name = request.args.get("last_name")
    email = request.args.get("email")
    password = request.args.get("password")
    return add_user(db, first_name, last_name, email, password)


def add_user(db, first_name, last_name, email, password):
    my_cursor = db.cursor()
    sql = "INSERT INTO users(name, last_name, email, password) VALUES (%s,%s,%s,%s);"
    my_cursor.execute(sql, (first_name, last_name, email, password))
    db.commit()
    db.close()
    return "successfully added"


if __name__ == '__main__':
    app.run(host="localhost", debug=True)
