from db_smart_groceries import create_connection

db = create_connection()
my_cursor = db.cursor()

create_table_shoppingcart = "CREATE TABLE shoppingcart (product VARCHAR(100), quantity INT UNSIGNED, first_name VARCHAR(50), last_name VARCHAR(50));"
create_table_teams = "CREATE TABLE teams (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, team_name VARCHAR(50), team_password VARCHAR(50));"
create_table_users = "CREATE TABLE users (name VARCHAR(100), last_name VARCHAR(100), email VARCHAR(50), password VARCHAR(50));"
alter_table = "ALTER TABLE users DROP COLUMN team_id"
describe_table = "DESCRIBE teams;"
truncate_table = "TRUNCATE TABLE teams;"
drop_table = "DROP TABLE teams"
show_table = "SELECT * FROM shoppingcart;"
show_all_tables = "SHOW TABLES;"
delete_table = "DROP TABLE teams"

my_cursor.execute(show_table)
for x in my_cursor:
    print(x)

db.commit()
db.close()
