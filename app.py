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

@app.route("/admin_login", methods=['GET','POST'])
def admin_login():
    return render_template('admin_login.html')

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route("/department_info",methods=['GET','POST'])
def department_info():
    msg=''
    if request.method == 'POST' and 'deptname' in request.form and 'cid' in request.form and 'cname' in request.form :
        deptname = request.form['deptname']
        cid = request.form['cid']
        cname = request.form['cname']
        if len(deptname) > 0 and len(cid) > 0 and len(cname) > 0:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM dept_cid_cname WHERE cid = % s AND deptname = %s', (cid,deptname, ) )
            record1 = cursor.fetchone()
            cursor.close()
            if record1 :
                msg='Record already exits!'
            elif not re.match(r'[A-Z0-9]+', cid):
                msg = 'Course Id must contain only Capital Letters and Numbers !'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO dept_cid_cname VALUES ( %s , %s , %s) ', (deptname,cid,cname, ) )
                mysql.connection.commit()
                cursor.close()
                msg='Record Added Successfully!'
        else:
            msg='Please fill out the form!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('department_info.html',msg=msg)

@app.route("/prof_info",methods=['GET','POST'])
def prof_info():
    msg=''
    if request.method == 'POST' and 'prof_name' in request.form and 'cid' in request.form  :
        prof_name = request.form['prof_name']
        cid = request.form['cid']
        if len(prof_name) > 0 and len(cid) > 0 :
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cid_pid_pname WHERE cid = % s AND prof_name = %s', (cid,prof_name, ) )
            record1 = cursor.fetchone()
            cursor.execute('SELECT * FROM dept_cid_cname WHERE cid = %s',(cid,))
            record2=cursor.fetchone()
            cursor.close()
            if record1 :
                msg='Record already exits!'
            elif not record2:
                msg=' This Course does not exist! Please add it first.'
            elif not re.match(r'[A-Z0-9]+', cid):
                msg = 'Course Id must contain only Capital Letters and Numbers !'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO cid_pid_pname VALUES (  NULL ,%s , %s) ', (cid,prof_name, ) )
                mysql.connection.commit()
                cursor.close()
                msg='Record Added Successfully!'
        else:
            msg='Please fill out the form!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('prof_info.html',msg=msg)

app.run(debug=True)
