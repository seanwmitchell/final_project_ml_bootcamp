# Libraries to import for database access
import json
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# with open('/etc/config.json') as config_file:
#     config = json.load(config_file)
# db_username = config.get('DB_USERNAME')
# db_password = config.get('DB_PASSWORD')

def db_check():

    # a function to check if we have the database established already. If no, call the setup functions.
    try:
        # Production
        # conn = psycopg2.connect("dbname=final_project host='localhost' user=" + db_username + " password=" + db_password)
        # Development
        conn = psycopg2.connect("dbname=final_project host='localhost' user='seanm'")
        conn.close()
    except:
        create_database()
        create_table()

def create_database():

    # a function to initially establish the database
    # Production
    # conn = psycopg2.connect("dbname=postgres host='localhost' user=" + db_username + " password=" + db_password)
    # Development
    conn = psycopg2.connect("dbname=postgres host='localhost' user='seanm'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql.SQL("CREATE DATABASE final_project\
            ").format(sql.Identifier('final_project')))
    conn.close()
    print("***** database setup.")

def create_table():

    # a function to create the table in the new db

    # Production
    # conn = psycopg2.connect("dbname=final_project host='localhost' user=" + db_username + " password=" + db_password)
    # Development
    conn = psycopg2.connect("dbname=final_project host='localhost' user='seanm'")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql.SQL("""CREATE TABLE stories(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            intro VARCHAR(255),
            body TEXT
            );"""))
    cur = conn.cursor()
    cur.execute(sql.SQL("""CREATE TABLE tags(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255)
            );"""))
    conn.close()
    print("***** table setup.")