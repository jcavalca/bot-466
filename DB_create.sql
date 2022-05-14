CREATE TABLE Teacher (Name VARCHAR(45) PRIMARY KEY, Room INTEGER, Building VARCHAR(65), Phone INT, Email VARCHAR(45), Title VARCHAR(45), OfficeHours VARCHAR(65), HowToConnect VARCHAR(65) );
CREATE TABLE Course (Prefix VARCHAR(5), Number INT, Title VARCHAR(65), Units INT, Prereq VARCHAR(255), Description TEXT, PRIMARY KEY (Prefix, Number) );
CREATE TABLE Section (CoursePrefix VARCHAR(65), CourseNumberPrefix INT, Number INT, Teacher VARCHAR(45), Type ENUM("Lab", "Lec", "Seminar"), Days VARCHAR(5), StartTime VARCHAR(8), EndTime VARCHAR(8), Room INT, Building VARCHAR(15), Quarter VARCHAR(6), Year INT, PRIMARY KEY (CoursePrefix, CourseNumberPrefix, Number, Quarter, Year), FOREIGN KEY (CoursePrefix, CourseNumberPrefix) REFERENCES Course (Prefix, Number), FOREIGN KEY (Teacher) REFERENCES Teacher (Name) )
CREATE TABLE PreReq (CoursePrefix VARCHAR(5), CourseNumber INT, PreReqPrefix VARCHAR(5), PreReqNumber INT, PRIMARY KEY (CourseNumber, CoursePrefix, PreReqPrefix, PreReqNumber));