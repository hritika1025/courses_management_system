CREATE DATABASE courses_management;
USE courses_management;
CREATE TABLE dept_cid_cname(
	deptname VARCHAR(100) NOT NULL,
    cid VARCHAR(100) NOT NULL,
    cname VARCHAR(100) NOT NULL,
    PRIMARY KEY(cid)
);
CREATE TABLE cid_pid_pname(
    cid VARCHAR(100) NOT NULL,
    prof_id INT NOT NULL,
    prof_name VARCHAR(200) NOT NULL,
    PRIMARY KEY(prof_id),
    FOREIGN KEY(cid) REFERENCES dept_cid_cname(cid)
);
CREATE TABLE pid_time(
    prof_id INT NOT NULL,
    time_slot VARCHAR(100) NOT NULL,
    room_num VARCHAR(50) NOT NULL,
    sem VARCHAR(50) NOT NULL,
    yr INT NOT NULL,
    PRIMARY KEY(time_slot, room_num, sem, yr),
    FOREIGN KEY(prof_id) REFERENCES cid_pid_pname(prof_id)
);

INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('CSE', 'CS-207', 'Database Management System');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('CSE', 'CS-203', 'Data Structures And Algorithm');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('CSE', 'CS-201', 'Discrete Maths');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('EE', 'EE-203', 'Electronic Devices');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('EE', 'EE-205', 'Network Theory');
INSERT INTO dept_cid_cname(deptname, cid, cname) VALUES('EE', 'EE-104', 'Basic Electrical and Electronics Engineering');

INSERT INTO cid_pid_pname(cid, prof_id, prof_name) VALUES('CS-207', 1, 'Nagendra Kumar');
INSERT INTO cid_pid_pname(cid, prof_id, prof_name) VALUES('EE-203', 2, 'Abhinav Kranti');
INSERT INTO cid_pid_pname(cid, prof_id, prof_name) VALUES('EE-104', 3, 'Abhinav Kranti');
INSERT INTO pid_time(prof_id, time_slot, room_num, sem, yr) VALUES(1, 'Monday 11:00-11:50', 'L-02', 'AUTUMN', 2021);
SELECT * FROM cid_pid_pname;
SELECT * FROM pid_time;
SELECT cname FROM dept_cid_cname WHERE deptname = 'EE' and cid in (SELECT cid FROM cid_pid_pname WHERE prof_id = (SELECT prof_id FROM pid_time WHERE sem = 'AUTUMN' AND yr = 2021));
SELECT cname FROM dept_cid_cname where deptname = 'EE' and cid in (SELECT cid FROM cid_pid_pname WHERE prof_name = 'Abhinav Kranti');
SELECT prof_name FROM cid_pid_pname WHERE cid in (SELECT cid FROM dept_cid_cname WHERE deptname = 'CSE' and cname = 'Database Management System');
SELECT cname FROM dept_cid_cname WHERE deptname='CSE';
