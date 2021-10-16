
CREATE DATABASE courses_management;
USE courses_management;
CREATE TABLE dept_cid_cname(
	deptname VARCHAR(100) NOT NULL,
    cid VARCHAR(100) NOT NULL,
    cname VARCHAR(100) NOT NULL,
    PRIMARY KEY(cid)
);
CREATE TABLE cid_pid_pname(
    prof_id INT NOT NULL AUTO_INCREMENT,
    cid VARCHAR(100) NOT NULL,
    prof_name VARCHAR(200) NOT NULL,
    PRIMARY KEY(prof_id),
    FOREIGN KEY(cid) REFERENCES dept_cid_cname(cid)
)AUTO_INCREMENT=1;
CREATE TABLE pid_time(
cid VARCHAR(100) NOT NULL,
    prof_id INT NOT NULL,
    time_slot VARCHAR(100) NOT NULL,
    room_num VARCHAR(50) NOT NULL,
    sem VARCHAR(50) NOT NULL,
    yr INT NOT NULL,
    PRIMARY KEY(time_slot, room_num, sem, yr),
    FOREIGN KEY(prof_id) REFERENCES cid_pid_pname(prof_id),
     FOREIGN KEY(cid) REFERENCES dept_cid_cname(cid)
);
CREATE TABLE admin( admin_id VARCHAR(100) NOT NULL,
                     password VARCHAR(100) NOT NULL);

INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('CSE', 'CS207', 'Database Management System');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('CSE', 'CS203', 'Data Structures And Algorithm');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('CSE', 'CS201', 'Discrete Maths');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('EE', 'EE203', 'Electronic Devices');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('EE', 'EE205', 'Network Theory');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('EE', 'EE104', 'Basic Electrical and Electronics Engineering');

INSERT INTO cid_pid_pname( prof_id, cid, prof_name) VALUES( 1,'CS207', 'Nagendra Kumar');
INSERT INTO cid_pid_pname( prof_id, cid, prof_name) VALUES( 2,'EE203', 'Abhinav Kranti');
INSERT INTO cid_pid_pname( prof_id, cid, prof_name) VALUES( 3,'EE104', 'Abhinav Kranti');
INSERT INTO pid_time(cid,prof_id, time_slot, room_num, sem, yr) VALUES('CS207',1, 'Monday 11:00-11:50', 'L-02', 'AUTUMN', 2021);

INSERT INTO admin(admin_id,password) VALUES('cse200001029@iiti.ac.in','Hritika123');
SELECT * FROM admin;
SELECT * FROM cid_pid_pname;
SELECT * FROM pid_time;
SELECT cname FROM dept_cid_cname WHERE deptname = 'EE' and cid in (SELECT cid FROM cid_pid_pname WHERE prof_id = (SELECT prof_id FROM pid_time WHERE sem = 'AUTUMN' AND yr = 2021));
SELECT cname FROM dept_cid_cname where deptname = 'EE' and cid in (SELECT cid FROM cid_pid_pname WHERE prof_name = 'Abhinav Kranti');
SELECT prof_name FROM cid_pid_pname WHERE cid in (SELECT cid FROM dept_cid_cname WHERE deptname = 'CSE' and cname = 'Database Management System');
SELECT cname FROM dept_cid_cname WHERE deptname='CSE';
