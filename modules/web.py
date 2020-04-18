import sqlite3
import logging
import os
from math import ceil

from flask import Flask, redirect, render_template, g, flash, request

app = Flask(__name__)

def init_web(monitor, port: int, database: str, debug: bool):
    global db_name, pm
    db_name = database
    pm = monitor

    if not debug:
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'

    app.secret_key = os.urandom(16)
    app.run(host='0.0.0.0', port=port, debug=debug)

# # # # # # #
#   Routes   #
# # # # # # #

@app.route('/')
def index():
    return redirect('/database/1')

@app.route('/database')
def database():
    return redirect('/database/1')

@app.route('/database/<page>')
def database_page(page):
    offset = (int(page) - 1) * 50
    cur = get_db().cursor()

    cur.execute("SELECT * FROM pastes")
    pages_left = ceil(len(cur.fetchall()) / 50)

    cur.execute("SELECT * FROM pastes ORDER BY date DESC LIMIT 50 OFFSET ?", [offset])

    return render_template('database.html', pastes=cur.fetchall(), cur_page=int(page), pages_left=pages_left, offset=offset)

@app.route('/database/search', methods=["POST"])
def database_search():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM pastes ORDER BY date DESC")

    keywords = request.form['keywords'].split()
    pastes = []

    for paste in cur.fetchall():
        if pm.check_if_keywords(paste[0], keywords):
            pastes.append(paste)

    return render_template('database.html', pastes=pastes, cur_page=0, pages_left=0, offset=0)

@app.route('/database/paste/<id>')
def database_paste(id):
    return '<pre>' + pm.get_raw_paste(id) + '</pre>'

@app.route('/database/delete/<id>')
def database_delete(id):
    cur = get_db().cursor()
    cur.execute("DELETE FROM pastes WHERE id = ?", [id])

    get_db().commit()
    flash("Paste deleted!")
    return redirect('/database')

@app.route('/clean')
def clean():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM pastes")

    for paste in cur.fetchall():
        unavailable = pm.check_if_unavailable(paste[0])

        if unavailable:
            cur.execute("DELETE FROM pastes WHERE id = ?", [paste[0]])
    
    get_db().commit()
    flash("Finished the clean up!")
    return redirect('/database')

# # # # # # #
#  Database  #
# # # # # # #

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name)
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()