from db_smart_groceries import create_connection

db = create_connection()
my_cursor = db.cursor()

create_table_shoppingcart = "CREATE TABLE shoppingcart (product_id INT PRIMARY KEY AUTO_INCREMENT, product VARCHAR(100), quantity INT UNSIGNED, first_name VARCHAR(50), last_name VARCHAR(50));"
create_table_teams = "CREATE TABLE teams (team_id INT PRIMARY KEY AUTO_INCREMENT, team_name VARCHAR(50), team_password VARCHAR(50));"
create_table_users = "CREATE TABLE users (user_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), last_name VARCHAR(100), email VARCHAR(50) UNIQUE, password VARCHAR(50));"
create_table_teams_users = "CREATE TABLE teams_users (group_id INT, user_id INT, CONSTRAINT U_ROW UNIQUE (group_id, user_id));"
# create_table_teams_shopping_cart = "CREATE TABLE teams_products (group_id INT, product_id INT, CONSTRAINT U_ROW UNIQUE (group_id, product_id));"
alter_table = "ALTER TABLE shoppingcart ADD team_id INT"
describe_table = "DESCRIBE shoppingcart;"
truncate_table = "TRUNCATE TABLE users;"
drop_table = "DROP TABLE teams_products"
show_table = "SELECT * FROM teams_users;"
show_all_tables = "SHOW TABLES;"
delete_table = "DROP TABLE teams"

my_cursor.execute(describe_table)
for x in my_cursor:
    print(x)

db.commit()
db.close()
