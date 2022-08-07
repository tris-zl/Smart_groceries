from db_smart_groceries import create_connection

db = create_connection()
my_cursor = db.cursor()

# my_cursor.execute("CREATE TABLE shoppingcart (product VARCHAR(100), quantity INT UNSIGNED, first_name VARCHAR(50), last_name VARCHAR(50))")
my_cursor.execute("DESCRIBE shoppingcart")
for x in my_cursor:
    print(x)

db.close()
