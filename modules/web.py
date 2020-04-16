import sqlite3

from flask import Flask, redirect, render_template, g

app = Flask(__name__)

def init_web(monitor, port: int, database: str):
    global db_name, pm
    db_name = database
    pm = monitor
    app.run(host='0.0.0.0', port=8100, debug=True)

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

    return redirect('/database')

@app.route('/logs')
def logs():
    return render_template('logs.html')

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