import flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify ,current_app  # übersetzt python-dicts in json
import sqlite3


app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message

@app.route('/', methods=['GET'])
def home():
    return "<h1>Tischreservierung</h1>"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
def connect_db():
    conn = sqlite3.connect('buchungssystem.sqlite')

    conn.row_factory = dict_factory
    cur = conn.cursor()

    with current_app.open_resource('create_buchungssystem.sql') as f:
        conn.executescript(f.read().decode('utf8'))

    return cur


@app.route('/api/Tischreservierung/tische/all', methods=['GET'])
def api_all_tische():
    cur=connect_db()
    alle_tische = cur.execute('SELECT * FROM tische;').fetchall()

    return jsonify(alle_tische)


@app.route('/api/Tischreservierung/reservierungen/all', methods=['GET'])
def api_all_reservierungen():
    cur=connect_db()

    alle_tische = cur.execute('SELECT * FROM reservierungen;').fetchall()

    return jsonify(alle_tische)



@app.route('/api/Tischreservierung/freie_tische', methods=['GET'])
def api_freie_tische():
    cur=connect_db()

    alle_tische = cur.execute('SELECT * FROM reservierungen;').fetchall()

    return jsonify(alle_tische)




@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404



app.run()
