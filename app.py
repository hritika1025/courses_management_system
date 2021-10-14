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
    prof_name=''
    deptname=''
    if request.method == 'POST' :
        deptname = request.form['deptname']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT cname FROM dept_cid_cname  WHERE deptname =% s', (deptname, )) 
        cursor.execute('SELECT  cid_pid_pname.prof_name FROM dept_cid_cname INNER JOIN cid_pid_pname on dept_cid_cname.cid = cid_pid_pname.cid WHERE deptname =% s', (deptname, )) 
        prof_name = cursor.fetchall() 
        cursor.close()
        # return redirect(url_for('course'))
    return render_template('index.html',prof_name=prof_name,deptname=deptname) 



app.run(debug=True)
