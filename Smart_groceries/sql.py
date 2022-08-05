import mysql.connector
from aifc import Error


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


db = create_connection()
my_cursor = db.cursor()

# my_cursor.execute("CREATE TABLE shoppingcart (product VARCHAR(100), quantity INT UNSIGNED, first_name VARCHAR(50), last_name VARCHAR(50))")
my_cursor.execute("DESCRIBE shoppingcart")
for x in my_cursor:
    print(x)

db.close()
