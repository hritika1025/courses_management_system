from configparser import ExtendedInterpolation
from re import A
# import cur as cur
from flask import Flask, render_template, request,session
from flask_mysqldb import MySQL
import mysql.connector
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = 'hritika1025'


myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "root",database="course_management", buffered=True)


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


@app.route('/sem_timetable',methods=['GET','POST'])
def sem_timetable():
    if request.method=='POST':
        queryDetails = request.form
        semester = request.form['semester']
        year = request.form['year']
        print(year,semester)
        Query = '''
        SELECT cf.Course_ID,c.Course_Name,c.Dept_Name,cf.Faculty_ID,f.Faculty_Name,tt.Weekday,tt.Start_Time,
               tt.End_Time,tt.Semester,tt.Room_Num,tt.Year
        FROM Course_Faculty cf 
        JOIN TimeTable tt on cf.Course_ID = tt.Course_ID  AND cf.Year = tt.Year AND cf.Semester = tt.Semester
        JOIN Faculty f on cf.Faculty_ID = f.Faculty_ID
        JOIN Course c on cf.Course_ID = c.Course_ID
        WHERE cf.Year=%s AND cf.Semester='%s' '''  %(int(year),semester)

        cur = myconn.cursor()
        cur.execute(Query)
        Details = cur.fetchall()
        # print(Details)
        return render_template('sem_timetable.html',courseDetails=Details)
    return render_template('sem_timetable.html',courseDetails='')

@app.route('/faculty_list/<string:dept_name>',methods =['GET', 'POST'])
def faculty_list(dept_name):
    session['dept_name_fac'] = dept_name
    if request.method=='POST':
        course=request.form['course']
        s_time=request.form['s_time']
        l_time = request.form['l_time']
        print(course)
        print(s_time)
        print(l_time)

        if int(s_time)==0:
            s_time=2009
        if int(l_time)==0:
            l_time=2021

        if course!='All':
            Query = '''
                    SELECT cf.Faculty_ID,f.Faculty_Name,cf.Year,cf.Semester
                    FROM Course_Faculty cf
                    JOIN Faculty f on cf.Faculty_ID = f.Faculty_ID
                    JOIN Course c on cf.Course_ID = c.Course_ID
                    WHERE cf.Year>=%s AND cf.Year<=%s AND c.course_Name='%s' ''' % (int(s_time), int(l_time),course)
            print(course)
        else:
            print("NOTHING")
            Query = '''SELECT cf.Faculty_ID,f.Faculty_Name,cf.Year,cf.Semester
                    FROM Course_Faculty cf
                    JOIN Faculty f on cf.Faculty_ID = f.Faculty_ID
                    JOIN Course c on cf.Course_ID = c.Course_ID and c.Dept_Name = '%s'
                    WHERE cf.Year>=%s AND cf.Year<=%s ''' % (session['dept_name_fac'],int(s_time), int(l_time))
        cur = myconn.cursor()
        cur.execute(Query)
        Details = cur.fetchall()
        print(Details)
        return render_template('faculty_list.html',check=True,faculty=Details,query_details=[course,s_time,l_time],d_name=session['dept_name_fac'])

    if session['dept_name_fac'] == 'none':
        return render_template('faculty_list.html',check=False,query_details=['','',''],d_name=session['dept_name_fac'])
    else:
        dept = session['dept_name_fac']
        cur = myconn.cursor()
        Query = '''SELECT Faculty_ID,Faculty_Name FROM Faculty WHERE dept_name='%s' ''' % (dept)

        cur = myconn.cursor()
        cur.execute(Query)
        data = cur.fetchall()
        Q = '''SELECT * FROM Course WHERE dept_name='%s' ''' % (dept)
        cur = myconn.cursor()
        cur.execute(Q)
        d = cur.fetchall()
        session['dept']=d
        return render_template('faculty_list.html',check=True,query_details=['','',''],d_name=session['dept_name_fac'])

@app.route('/course_list/<string:dept_name>', methods = ['GET', 'POST'])
def course_list(dept_name):
    session['dept_name_course'] = dept_name
    if request.method == 'POST':
        faculty = request.form.get('faculty')
        start_year = request.form.get('start_year')
        end_year = request.form.get('end_year')

        if start_year == 'None':
            start_year=2011
        else:
            start_year=int(start_year)

        if end_year == 'None':
            end_year=2020
        else:
            end_year=int(end_year)

        if faculty == 'None':
            cur = myconn.cursor()
            query = "SELECT * FROM course WHERE Dept_Name='%s' " % (session['dept_name_course'])
            cur.execute(query)
            course = cur.fetchall()
            course = list(set(course))
        else:
            cur1 = myconn.cursor()
            query1 = "SELECT course.Course_ID, course.Course_Name FROM course INNER JOIN course_faculty ON course.Course_ID = course_faculty.Course_ID AND course.Dept_Name = '%s' AND course_faculty.faculty_ID = '%s' AND course_faculty.Year>='%s' AND course_faculty.Year<='%s' " % (session['dept_name_course'], faculty, start_year, end_year)
            cur1.execute(query1)
            course = cur1.fetchall()
            course = list(set(course))
        return render_template('course_list.html', check=True, course=course,d_name=session['dept_name_course'])

    if session['dept_name_course']=='none':
        return render_template('course_list.html',check=False,course=None,d_name=session['dept_name_course'])

    else:
        dept = session['dept_name_course']
        cur = myconn.cursor()
        query = "SELECT * FROM course WHERE Dept_Name='%s' " % (dept)
        cur.execute(query)
        course = cur.fetchall()
        query1 = "SELECT faculty.Faculty_Name, faculty.Faculty_ID FROM faculty INNER JOIN course_faculty ON faculty.Faculty_ID = course_faculty.Faculty_ID AND faculty.Dept_Name = '%s' " %(dept)
        cur1 = myconn.cursor()
        cur1.execute(query1)
        faculty = cur1.fetchall()
        session['faculty'] = list(set(faculty))
        session['dept'] = dept
        return render_template('course_list.html', check=True, course=course,d_name=session['dept_name_course'])

cur = myconn.cursor()

def update_dep_list():
    cur.execute('SELECT * FROM department')
    dept_list = cur.fetchall()
    return dept_list

# dept_list = update_dep_list()

@app.route('/addEntry')
def home():
    dept_list = update_dep_list()
    return render_template('add.html', dept_list=dept_list)

@app.route('/add-department', methods=['GET', 'POST'])
def add_department():
    dept = ""
    if request.method == "POST":
        dept_name = request.form.get('dept_name')
        dept_name = dept_name.upper()
        cur.execute('SELECT * FROM department WHERE Dept_Name = %s', (dept_name, ))
        present = cur.fetchone()
        if present == None:
            cur.execute('INSERT INTO department VALUES (%s)', (dept_name, ))
            myconn.commit()
            # dept_list = update_dep_list()
            dept = "Added Successfully!!"
        else:
            dept = "Department is already present in the database"
    dept_list = update_dep_list()
    return render_template('add.html', dept=dept, dept_list=dept_list)

@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    crs = ""
    if request.method == "POST":
        dept_name = request.form.get('dept_name')
        course_id = request.form.get('course_id')
        course_name = request.form.get('course_name')
        cur.execute('SELECT * FROM course WHERE Course_ID = %s', (course_id, ))
        course_id_present = cur.fetchone()
        if course_id_present == None:
            cur.execute('INSERT INTO course VALUES (%s, %s, %s)', (course_id, course_name, dept_name, ))
            myconn.commit()
            crs = "Added Successfully!!"
        else:
            crs = "There is already a course with this Course ID"
    dept_list = update_dep_list()
    return render_template('add.html', crs=crs, dept_list=dept_list)

@app.route('/add-faculty', methods=['GET', 'POST'])
def add_faculty():
    fac = ""
    if request.method == "POST":
        dept_name = request.form.get('dept_name')
        faculty_id = request.form.get('faculty_id')
        faculty_name = request.form.get('faculty_name')
        cur.execute('SELECT * FROM faculty WHERE Faculty_ID = %s', (faculty_id, ))
        faculty_id_present = cur.fetchone()
        if faculty_id_present == None:
            cur.execute('INSERT INTO faculty VALUES (%s, %s, %s)', (faculty_id, faculty_name, dept_name, ))
            myconn.commit()
            fac = "Added Successfully!!"
        else:
            fac = "There is already a faculty present with this Faculty ID"
    dept_list = update_dep_list()
    return render_template('add.html', fac=fac, dept_list=dept_list)

@app.route('/add-course-faculty', methods=['GET', 'POST'])
def add_course_faculty():
    adcf = ""
    faculty_id = request.form.get('faculty_id')
    course_id = request.form.get('course_id')
    year = request.form.get('year')
    semester = request.form.get('semester')
    students = request.form.get('students')
    cur.execute('SELECT * FROM faculty WHERE Faculty_ID = %s', (faculty_id, ))
    faculty_id_present = cur.fetchone()
    if faculty_id_present == None:
        adcf = "There is no faculty with this Faculty ID in database"
    else:
        cur.execute('SELECT * FROM course WHERE Course_ID = %s', (course_id, ))
        course_id_presesnt = cur.fetchone()
        if course_id_presesnt == None:
            adcf = "There is no course with this Course ID in database"
        else:
            cur.execute('SELECT * FROM course_faculty WHERE Course_ID = %s AND Faculty_ID = %s AND Year = %s AND Semester = %s', (course_id, faculty_id, year, semester, ))
            query_present = cur.fetchone()
            if query_present == None:
                cur.execute('INSERT INTO course_faculty VALUES (%s, %s, %s, %s, %s)', (course_id, faculty_id, year, semester, students, ))
                myconn.commit()
                adcf = "Added Successfully!!"
            else:
                adcf = "Please don't make redundant entries"
    dept_list = update_dep_list()
    return render_template('add.html', adcf=adcf, dept_list=dept_list)

@app.route('/add-classes', methods=['GET', 'POST'])
def add_classes():
    adcl = ""
    course_id = request.form.get('course_id')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    year = request.form.get('year')
    weekday = request.form.get('weekday')
    room_no = request.form.get('room_no')
    semester = request.form.get('semester')
    # faculty_id = request.form.get('faculty_id')
    cur.execute('SELECT * FROM course_faculty WHERE Course_ID = %s AND Year = %s AND Semester = %s', (course_id, year, semester, ))
    entry_present_in_course_has_faculty = cur.fetchone()
    if entry_present_in_course_has_faculty == None:
        adcl = "Please first add course with faculty"
    else:
        cur.execute('SELECT * FROM timetable WHERE Course_ID = %s AND Start_Time = %s AND End_Time = %s AND Year = %s AND Weekday = %s AND Room_Num = %s AND Semester = %s', (course_id, start_time, end_time, year, weekday, room_no, semester, ))
        query_present = cur.fetchone()
        if query_present == None:
            cur.execute('SELECT * FROM timetable WHERE Year = %s AND Weekday = %s AND Room_Num = %s AND Semester = %s AND ((Start_Time < %s AND Start_Time > %s) OR (End_Time > %s AND End_Time < %s) OR (Start_Time > %s AND End_Time < %s) OR (Start_Time <= %s AND End_Time >= %s))', (year, weekday, room_no, semester, end_time, start_time, start_time, end_time, start_time, end_time, start_time, end_time, ))
            conflicting_time = cur.fetchone()
            if conflicting_time != None:
                adcl = "Entries you made are conflicting"
            else:
                cur.execute('INSERT INTO timetable(Course_ID,Start_Time,End_Time,Year,Weekday,Room_Num,Semester) VALUES (%s, %s, %s, %s, %s, %s, %s)',(course_id, start_time, end_time, int(year), weekday, room_no, semester))
                myconn.commit()
                adcl = "Added Successfully!!"
        else:
            adcl = "Please don't make redundant entries"
    dept_list = update_dep_list()
    return render_template('add.html', adcl=adcl, dept_list=dept_list)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    return render_template('edit.html')

@app.route('/delete_course_faculty', methods=['GET', 'POST'])
def delete_course_faculty():
    if request.method=='POST':
        
        deltYear = request.form['deltYear']
        deltSemester = request.form['deltSemester']
        deltCID = request.form['deltCID']
        deltFID = request.form['deltFID']
        print(deltYear,deltSemester,deltCID,deltFID)

        if deltSemester!='Both':
            query1 = ''' DELETE FROM TimeTable
                WHERE Course_ID = '%s' and Year=%s and Semester='%s'
                ''' % (deltCID,deltYear,deltSemester)
            query2 = ''' DELETE FROM Course_Faculty 
                WHERE Course_ID = '%s' and Faculty_ID = '%s' and Year=%s and Semester='%s'
                ''' % (deltCID,deltFID,deltYear,deltSemester)
        else:
            query1 = ''' DELETE FROM TimeTable
                WHERE Course_ID = '%s' and Year=%s
                ''' % (deltCID,deltYear)
            query2 = ''' DELETE FROM Course_Faculty 
                WHERE Course_ID = '%s' and Faculty_ID = '%s' and Year=%s
                ''' % (deltCID,deltFID,deltYear)
        
        cur = myconn.cursor()
        cur.execute(query1)
        myconn.commit()
        cur.execute(query2)
        myconn.commit()

    return render_template('edit.html')

@app.route('/edit_timetable', methods=['GET', 'POST'])
def edit_timetable():
    if request.method=='POST':
        editDetails = request.form
        editYear = editDetails['editYear']
        editSemester = editDetails['editSemester']
        editCID = editDetails['editCID']
        
        query = '''SELECT * FROM TimeTable 
            WHERE Course_ID = '%s' and Year = %s and Semester = '%s'
            ''' %(editCID,editYear,editSemester)

        getCourseName = '''SELECT Course_Name FROM Course 
            WHERE Course_ID = '%s'
            ''' %(editCID)

        session['editCID'] = editCID
        session['editYear'] = editYear
        session['editSemester'] = editSemester
        
        cur = myconn.cursor()
        cur.execute(query)
        currTimeTable = cur.fetchall()
        myconn.commit()

        cur.execute(getCourseName)
        currCourseName = (cur.fetchall())[0][0]
        myconn.commit()

        inputDetails = [currCourseName,editCID,editYear,editSemester]
        
        return render_template('update_timetable.html',currTimeTable=currTimeTable,inputDetails=inputDetails)

    return render_template('edit.html')

@app.route('/updateTimeTable/<int:Time_ID>', methods=['GET', 'POST'])
def updateTimetable(Time_ID):
    if request.method=='POST':
        updtateDetails = request.form
        cid = session['editCID']
        year = session['editYear']
        semester = session['editSemester']

        s_time = updtateDetails['s_time']
        e_time = updtateDetails['e_time']
        weekday = updtateDetails['weekday']
        room_no = updtateDetails['room_no']

        if s_time!='':
            print("Start Time",s_time)
            query = '''UPDATE TimeTable SET Start_Time = '%s'  
                    WHERE Course_ID='%s' and Year=%s and Semester='%s' and Time_ID = %s ''' %(s_time,cid,year,str(semester),int(Time_ID))
            
            cur = myconn.cursor()
            cur.execute(query)
            myconn.commit()
        else:
            print("No s_time")

        if e_time!='':
            query = '''UPDATE TimeTable SET End_Time = '%s'  
                    WHERE Course_ID='%s' and Year=%s and Semester='%s' and Time_ID = %s
                    ''' %(e_time,cid,year,str(semester),int(Time_ID))
            cur = myconn.cursor()
            cur.execute(query)
            myconn.commit()
        else:
            print("No e_time")
        
        if weekday!='':
            query = '''UPDATE TimeTable SET Weekday = '%s'  
                    WHERE Course_ID='%s' and Year=%s and Semester='%s' and Time_ID = %s
                    ''' %(weekday,cid,int(year),semester,int(Time_ID))
            cur = myconn.cursor()
            cur.execute(query)
            myconn.commit()
        else:
            print("No weekday")

        if room_no!='':
            query = '''UPDATE TimeTable SET Room_Num = '%s'  
                    WHERE Course_ID='%s' and Year=%s and Semester='%s' and Time_ID = %s
                    ''' %(room_no,cid,int(year),semester,int(Time_ID))
            cur = myconn.cursor()
            cur.execute(query)
            myconn.commit()
        else:
            print("No room_no")

    editCID = session['editCID']
    editYear = session['editYear']
    editSemester = session['editSemester']

    query = '''SELECT * FROM TimeTable 
            WHERE Course_ID = '%s' and Year = %s and Semester = '%s'
            ''' %(editCID,editYear,editSemester)

    getCourseName = '''SELECT Course_Name FROM Course 
            WHERE Course_ID = '%s'
            ''' %(editCID)

    cur = myconn.cursor()
    cur.execute(query)
    currTimeTable = cur.fetchall()
    myconn.commit()

    cur.execute(getCourseName)
    currCourseName = (cur.fetchall())[0][0]
    myconn.commit()

    inputDetails = [currCourseName,editCID,editYear,editSemester]

    return render_template('update_timetable.html',currTimeTable=currTimeTable,inputDetails=inputDetails)

@app.route('/deleteRow/<int:Time_ID>', methods=['GET', 'POST'])
def deleteRow(Time_ID):
    query = '''DELETE FROM TimeTable
            WHERE Time_ID=%s'''%(Time_ID)

    cur= myconn.cursor()
    cur.execute(query)
    myconn.commit()
    editCID = session['editCID']
    editYear = session['editYear']
    editSemester = session['editSemester']

    query = '''SELECT * FROM TimeTable 
            WHERE Course_ID = '%s' and Year = %s and Semester = '%s'
            ''' %(editCID,editYear,editSemester)

    getCourse = '''SELECT Course_Name FROM Course 
            WHERE Course_ID = '%s'
            ''' %(editCID)

    cur = myconn.cursor()
    cur.execute(query)
    currTimeTable = cur.fetchall()
    myconn.commit()

    cur.execute(getCourse)
    currCourse = (cur.fetchall())[0][0]
    myconn.commit()

    inputDetails = [currCourse,editCID,editYear,editSemester]

    return render_template('update_timetable.html',currTimeTable=currTimeTable,inputDetails=inputDetails)
    

        
if __name__ == '__main__':
    app.run(debug=True, port=8000)
