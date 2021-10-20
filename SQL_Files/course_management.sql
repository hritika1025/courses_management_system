DROP DATABASE course_management;
CREATE DATABASE IF NOT EXISTS course_management;
USE  course_management;
CREATE TABLE IF NOT EXISTS `Department` (
  `Dept_Name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`Dept_Name`));

CREATE TABLE IF NOT EXISTS `Course` (
  `Course_ID` VARCHAR(100) NOT NULL,
  `Course_Name` VARCHAR(100) NULL DEFAULT NULL,
  `Dept_Name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`Course_ID`), 
  FOREIGN KEY (`Dept_Name`) REFERENCES `Department` (`Dept_Name`) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS `Faculty` (
  `Faculty_ID` VARCHAR(100) NOT NULL,
  `Faculty_Name` VARCHAR(100) NOT NULL,
  `Dept_Name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`Faculty_ID`),
  FOREIGN KEY (`Dept_Name`) REFERENCES `Department` (`Dept_Name`) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS `Course_Faculty` (
  `Course_ID` VARCHAR(100) NOT NULL,
  `Faculty_ID` VARCHAR(100) NOT NULL,
  `Year` INT,
  `Semester` VARCHAR(100),
  `Students` INT,
  PRIMARY KEY (`Course_ID`, `Faculty_ID`,`Year`,`Semester`),
  KEY(`Course_ID`),
   KEY(`Year`),
   KEY(`Semester`),
   KEY(`Course_ID`,`Year`,`Semester`),
  FOREIGN KEY (`Course_ID`) REFERENCES `Course` (`Course_ID`) ON DELETE CASCADE,
 FOREIGN KEY (`Faculty_ID`) REFERENCES `Faculty` (`Faculty_ID`) ON DELETE CASCADE);
    
    
CREATE TABLE IF NOT EXISTS `TimeTable` (
  `Time_ID` INT AUTO_INCREMENT,
  `Course_ID` VARCHAR(100) NOT NULL,
  `Start_Time` TIME,
  `End_Time` TIME,
  `Year` INT ,
  `Weekday` VARCHAR(100) ,
  `Room_Num` VARCHAR(100) ,
  `Semester` VARCHAR(100) ,
  KEY (`Time_ID`),
  PRIMARY KEY(`Course_ID`,`Start_Time`,`End_Time`,`Year`,`Weekday`,`Room_Num`,`Semester`),
 FOREIGN KEY (`Course_ID`,`Year`,`Semester`) REFERENCES `Course_Faculty` (`Course_ID`,`Year`,`Semester`) ON DELETE CASCADE
);

INSERT INTO `Department` (Dept_Name)
VALUES
('Computer Science and Engineering'),('Mechanical Engineering'),('Electrical Engineering'),('Civil Engineering'),('Metallurgical Engineering And Material Science');

INSERT INTO `Course` (Course_ID,Course_Name,Dept_Name)
VALUES
('CS203','Data_Structures_And_Algorithm','Computer Science and Engineering'),
('ME201','Solid_Mechanics','Mechanical Engineering'),
('ME203','Fluid_Mechanics','Mechanical Engineering'),
('ME257','Machine_Drawing','Mechanical Engineering'),
('CS201','Discrete_Mathematical_Structures','Computer Science and Engineering'),
('CS207','Database_&_Information_Systems','Computer Science and Engineering'),
('EE201','Network_Theory','Electrical Engineering'),
('MM203','Physical_Metallurgy-I','Metallurgical Engineering And Material Science'),
('MM205','Materials_Science','Metallurgical Engineering And Material Science'),
('CE202','Structural_Mechanics-I','Civil Engineering'),
('CE201','Solid_Mechanics-I','Civil Engineering'),
('EE203','Electronic_Devices','Electrical Engineering');

INSERT INTO `Faculty` (Faculty_ID,Faculty_Name,Dept_Name)
VALUES
('FACS1','Dr. Puneet Gupta','Computer Science and Engineering'),
('FAME1','Dr. Kalandi C Pradhan','Mechanical Engineering'),
('FACS2','Dr. Nagendra Kumar','Computer Science and Engineering'),
('FAEE1','Prof. Anjan Chakraborty','Electrical Engineering'),
('FAMEMS1','Dr. Selvakumar Sermadurai','Metallurgical Engineering And Material Science'),
('FACE1','Dr. Guru Prakash','Civil Engineering'),
('FAEE2','Prof. Abhinav Raghuvanshi','Electrical Engineering'),
('FACS3','Dr. Narendra S. Chaudhary','Computer Science and Engineering'),
('FAME2','Dr. Sumit S. Chaudhary','Mechanical Engineering'),
('FACS4','Abhishek Srivastava','Computer Science and Engineering'),
('FAEE3','Prof. Vinay Kumar Gupta','Electrical Engineering'),
('FAMEMS2','Dr. Priyansh Singh','Metallurgical Engineering And Material Science'),
('FACE2','Prof. Sandeep Chaudhary','Civil Engineering'),
('FACE3','Dr. Priyansh Singh','Civil Engineering');

INSERT INTO `Course_Faculty` (Course_ID,Faculty_ID,Year,Semester,Students)
VALUES
('CE201','FACE1',2014,'Autumn',55),
('CS203','FACS1',2012,'Spring',45),
('ME201','FAME1',2011,'Autumn',11),
('CS207','FACS2',2015,'Spring',22),
('CE201','FACE2',2016,'Spring',46),
('CS203','FACS1',2011,'Autumn',35),
('CS201','FACS3',2014,'Spring',58),
('MM203','FAMEMS1',2017,'Autumn',39),
('CE202','FACE1',2015,'Spring',41),
('CE201','FACE1',2011,'Autumn',22),
('CE202','FACE3',2012,'Spring',31),
('MM205','FAMEMS1',2013,'Autumn',75),
('EE203','FAEE2',2011,'Spring',56),
('CS207','FACS2',2013,'Spring',65),
('MM203','FAMEMS1',2014,'Autumn',80),
('EE203','FAEE2',2016,'Autumn',13),
('MM205','FAMEMS1',2015,'Spring',44),
('EE201','FAEE3',2019,'Autumn',44),

('EE203','FAEE3',2013,'Spring',50),
('EE201','FAEE3',2013,'Autumn',55);


INSERT INTO `TimeTable` (Course_ID,Start_Time,End_Time,Year,Weekday,Room_Num,Semester)
VALUES
('CS207','08:00:00','10:00:00',2015,'Monday','L103','Spring'),
('CS207','08:00:00','10:00:00',2015,'Tuesday','L103','Spring'),
('CS207','08:00:00','10:00:00',2015,'Wednesday','L103','Spring'),
('EE203','10:00:00','11:50:00',2011,'Wednesday','L102','Spring'),
('EE203','10:00:00','11:50:00',2011,'Thursday','L102','Spring'),
('CE201','09:00:00','09:50:00',2011,'Thursday','L111','Autumn'),
('CE201','09:00:00','09:50:00',2011,'Friday','L111','Autumn'),
('CE201','09:00:00','09:50:00',2011,'Saturday','L111','Autumn'),
('MM205','07:00:00','09:00:00',2015,'Thursday','POD101','Spring'),
('MM205','06:00:00','08:00:00',2015,'Friday','POD102','Spring'),
('MM205','08:00:00','10:00:00',2015,'Saturday','POD103','Spring'),

('EE203','11:24:00','12:36:00',2013,'Saturday','KOD111','Spring'),
('EE203','11:24:00','12:36:00',2013,'Sunday','KOD111','Spring'),
('EE201','11:24:00','12:36:00',2013,'Saturday','KOD111','Autumn'),
('EE201','11:24:00','12:36:00',2013,'Sunday','KOD111','Autumn');
