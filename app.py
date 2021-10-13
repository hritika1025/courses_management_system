from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = 'hritika'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'courses_management'
 
mysql = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    cname=''
    if request.method == 'POST' and 'username' in request.form:
        deptname = request.form['deptname']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT cname FROM dept_cid_cname  WHERE deptname =% s', (deptname, )) 
        cname = cursor.fetchall() 
    return render_template('index.html',cname=cname)

app.run(debug=True)
