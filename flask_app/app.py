# Importing the libraries
import json
import os
from flask import Flask, render_template, request, redirect, send_from_directory
from db_admin import db_check
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import spacy
nlp = spacy.load("en_core_web_sm")
from bs4 import BeautifulSoup
import inflection

with open('/etc/config.json') as config_file:
    config = json.load(config_file)
db_username = config.get('DB_USERNAME')
db_password = config.get('DB_PASSWORD')

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
    conn = psycopg2.connect("dbname=final_project host='localhost' user=" + db_username + " password=" + db_password)
    # Development
    # conn = psycopg2.connect("dbname=final_project host='localhost' user='seanm'")

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

    # Production
    conn = psycopg2.connect("dbname=final_project host='localhost' user=" + db_username + " password=" + db_password)
    # Development
    # conn = psycopg2.connect("dbname=final_project host='localhost' user='seanm'")

    cur = conn.cursor()
    query = f"""
    SELECT * FROM stories WHERE id = {int(story_id)};
    """
    cur.execute(query)
    story = cur.fetchall()[0]

    corpora = story[1] + ". " + story[2] + ". " + story[3]

    corpora_sans_html = BeautifulSoup(corpora, "lxml").text

    final_corpora = corpora_sans_html.replace("'","").replace('"',"").replace('(',"").replace(')',"")

    doc = nlp(final_corpora)
    
    # Iterate through named entities
    people = set()
    locations = set()
    tags = set()
    discarded = set()
    for ent in doc.ents:
        
        # Filter our unneeded named entities
        if ent.label_ == "PERSON" and len(ent.text.split()) > 1:

            # Singularize the word
            # word = inflection.singularize(ent.text)
            word = ent.text
            
            
            # Capitalize the first letter without impacting the rest
            people.add(word[0].capitalize() + word[1:])
        # Filter our unneeded named entities
        
        elif ent.label_ == "PRODUCT" or ent.label_ == "ORG" or ent.label_ == "ORDINAL" or ent.label_ == "EVENT" or ent.label_ == "NORP":

            # Singularize the word
            # word = inflection.singularize(ent.text)
            word = ent.text
            
            # Capitalize the first letter without impacting the rest
            tags.add(word[0].capitalize() + word[1:])
        
        elif ent.label_ == "GPE":

            # Singularize the word
            # word = inflection.singularize(ent.text)
            word = ent.text
            
            # Capitalize the first letter without impacting the rest
            locations.add(word[0].capitalize() + word[1:])

        else:

            # Singularize the word
            # word = inflection.singularize(ent.text)
            word = ent.text
            
            # Capitalize the first letter without impacting the rest
            discarded.add(word[0].capitalize() + word[1:])



    matched_tags = set()
    for tag in tags:
        cur.execute(f"SELECT COUNT(*) FROM tags WHERE name ILIKE '{tag}';")
        if cur.fetchall()[0][0] > 0:
            matched_tags.add(tag)

    conn.close()

    potential_tags = set(tags.difference(matched_tags))

    return render_template('show.html', story=story, potential_tags=potential_tags, people=people, locations=locations, matched_tags=matched_tags, discarded=discarded)

if __name__ == '__main__':
    application.run(debug=True)