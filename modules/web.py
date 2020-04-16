import sqlite3
import logging
import os

from flask import Flask, redirect, render_template, g

app = Flask(__name__)

def init_web(monitor, port: int, database: str, debug: bool):
    global db_name, pm
    db_name = database
    pm = monitor

    if not debug:
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'

    app.run(host='0.0.0.0', port=port, debug=debug)

# # # # # # #
#   Routes   #
# # # # # # #

@app.route('/')
def index():
    return redirect('/database')

@app.route('/database')
def database():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM pastes ORDER BY date DESC")

    return render_template('database.html', pastes=cur.fetchall())

@app.route('/database/<keywords>')
def database_search(keywords):
    return render_template('database.html')

@app.route('/database/paste/<id>')
def database_paste(id):
    return '<pre>' + pm.get_raw_paste(id) + '</pre>'

@app.route('/database/delete/<id>')
def database_delete(id):
    cur = get_db().cursor()
    cur.execute("DELETE FROM pastes WHERE id = ?", [id])

    get_db().commit()
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