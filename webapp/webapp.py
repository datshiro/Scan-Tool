from flask import Flask, render_template, jsonify, abort, make_response, redirect, url_for, request
import json
import requests

#
# own package
#
import config
import pymysql


app = Flask(__name__)


def connect_db():
    return pymysql.connect(
        user='root', password='root', database='dvwa',
        autocommit=True, charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/scan', methods=['POST','GET'])
def scan():

    list_scan = []
    for scan in request.json.get('list_scan'):
        print (scan)
        list_scan.append(str(scan))

    url = request.json.get('url')

    payload = {"list_scan":list_scan, "url":url}
    
    server_api = config.SERVER_API
    request_api = requests.post(server_api+'/scan', data=payload)
    try:
        print (payload)
        print (request_api.json())
    except:
        pass
    return (jsonify(request_api.json()))


@app.route('/login/', methods=['POST','GET'])
def login():
    output = ""
    if request.method == 'POST':
        username = request.form['username']
        # password = request.form['password']
        print("username",username)
        db = connect_db()
        cursor = db.cursor()
        # "1' or '1'=1#"
        # "1' or '1'='1"
        # "tuyen' or 1 ='1 #"

        # query = "SELECT name FROM user where username='" + username + "'"
        # print("query", query)
        # cursor.execute(query)
        # cursor.execute("""SELECT username, name FROM user where username='%s' and password='%s';"""%(username,password))
        cursor.execute("""SELECT username, name FROM user where username='%s';"""%(username))
        row = cursor.fetchone()

        print("row", row)

        if row:
            for r in row:
                output += str(row[r]) + "\n"
                # output += str(r['name']) + "\n"
        else:
            output = "Username is missing from the database."
    return render_template('login.html', output=output)
    pass


def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS user2(
            id INTEGER PRIMARY KEY,
            username VARCHAR(32) NOT NULL,
            password VARCHAR(32) NOT NULL,
            name VARCHAR(254) NOT NULL
            )''')
    conn.commit()
    conn.close()


def init_data():
    users = [
        (1,'tuyen', '123456', 'Phan Thi Ngoc Tuyen'),
        (2,'khoa', '123456', 'Vang Dang Khoa'),
        (3,'dat', '123456', 'Nguyen Quoc Dat')
    ]

    conn = connect_db()
    cur = conn.cursor()
    for u in users:
        print("u", u)
        cur.execute("""INSERT INTO `user2` VALUES({},'{}','{}','{}');""".format(u[0], u[1], u[2], u[3]))
    # cur.executemany('INSERT INTO `user2` VALUES(?,?,?)', users)
    conn.commit()
    conn.close()


def init():
    create_tables()
    init_data()


if __name__ == '__main__':
    # init()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
