# Importing the libraries

import os
from flask import Flask, render_template, request, redirect, send_from_directory
from db_admin import db_check
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# with open('/etc/config.json') as config_file:
#     config = json.load(config_file)
# db_username = config.get('DB_USERNAME')
# db_password = config.get('DB_PASSWORD')

db_check()

application = Flask(__name__)

# Establishing the two folders
dir_path = os.path.dirname(os.path.realpath(__file__))
STATIC_FOLDER = 'static'

# Serving the index page
@application.route('/')
def index():
    return render_template('index.html')

@application.route('/save', methods=['POST'])
def save():

    # Production
    # conn = psycopg2.connect("dbname=final_project host='localhost' user=" + db_username + " password=" + db_password)
    # Development
    conn = psycopg2.connect("dbname=final_project host='localhost' user='seanm'")

    cur = conn.cursor()
    query = f"""
    INSERT INTO stories (title, intro, body) 
    VALUES (%s, %s, %s) RETURNING id;
    """
    val = (request.form.get('title'), request.form.get('intro'), request.form.get('body'))
    cur.execute(query, val)
    conn.commit()
    story_id = str(cur.fetchall()[0][0])
    cur.close()

    return redirect("/show/" + story_id, code = 302)

# # Serving the index page
@application.route('/show/<story_id>')
def show(story_id):

#     # Production
#     # conn = psycopg2.connect("dbname=final_project host='localhost' user=" + db_username + " password=" + db_password)
#     # Development
    conn = psycopg2.connect("dbname=final_project host='localhost' user='seanm'")

    cur = conn.cursor()
    query = f"""
    SELECT * FROM stories WHERE id = %s;
    """
    val = (story_id)
    cur.execute(query, val)
    stories = cur.fetchall()
    conn.close()

    return render_template('show.html', stories=stories)

if __name__ == '__main__':
    application.run(debug=True)