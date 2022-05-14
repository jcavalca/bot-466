from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

# connection = pymysql.connect(
#                 user     = "jcavalca466",
#                 password = "jcavalca466985",
#                 host     = "localhost",
#                 db       = "jcavalca466"
# )

class Course:
    '''Represents our Course table'''
    def __init__(self, prefix, number, title, units, prereq, description):
        '''Creates a Course'''
        self.prefix = prefix
        self.number = number
        self.title = title
        self.units = units
        self.prereq = prereq
        self.description = description
        self.insert()

    # inserts into DB
    def insert(self):
        '''Inserts Course into DB'''
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO Course (Prefix, Number, Title, Units, Prereq, Description) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, [self.prefix, self.number, self.title, self.units, self.prereq, self.descriptioin])

    def __repr__(self) -> str:
        s0 = self.prefix + self.number+"\n"
        s1 = "Prefix: " + self.prefix + "\n"
        s2 = "Number: " + self.number + "\n"
        s3 = "Title: " + self.title + "\n"
        s4 = "Units: " + self.units + "\n"
        s5 = "Prereq: " + self.prereq + "\n"
        s6 = "Description: " + self.description + "\n"
        return s0+s1+s2+s3+s4+s5+s6 

class PreReq:
    '''Represents our PreReq table'''

    def __init__(self, course_prefix, course_number, pre_req_prefix, pre_req_number):
        '''Creates a PreReq'''
        self.course_prefix = course_prefix
        self.course_number = course_number
        self.pre_req_prefix = pre_req_prefix
        self.pre_req_number = pre_req_number

    # inserts into DB
    def insert(self):
        '''Inserts PreReq into DB'''
        

class Section:
    '''Represents our Section table'''

    def __init__(self, course_prefix, course_number_prefix, number, teacher, section_type, days, start_time, end_time, room, building, quarter, year):
        '''Creates a Section'''
        self.course_prefix = course_prefix
        self.course_number_prefix = course_number_prefix
        self.number = number
        self.teacher = teacher
        self.section_type = section_type
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
        self.building = building
        self.quarter = quarter
        self.year = year

    def __repr__(self) -> str:
        s1 = "Course Prefix: " + self.course_prefix + "\n"
        s2 = "Course Number: " + self.course_number_prefix + "\n"
        s2 = "Section Number: " + self.number + "\n"
        s3 = "Teacher: " + self.teacher + "\n"
        s4 = "Type: " + self.section_type + "\n"
        s5 = "Days: " + self.days + "\n"
        s6 = "Start Time: " + self.start_time + "\n"
        s7 = "End Time: " + self.end_time + "\n"
        s8 = "Room: " + self.room + "\n"
        s9 = "Building: " + self.building + "\n"
        s10 = "Quarter: " + self.quarter + "\n"
        s11 = "Year: " + self.year + "\n"
        return s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+s11
        
    # inserts into DB
    def insert(self):
        '''Inserts Section into DB'''
        with connection.cursor() as cursor:

            # Creates table, if necessary
            cursor.execute("CREATE TABLE IF NOT EXISTS Section \
                (CoursePrefix VARCHAR(65), CourseNumberPrefix INT, Number INT, \
                Teacher VARCHAR(45), Type ENUM('Lab', 'Lec', 'Sem'), \
                Days VARCHAR(5), StartTime VARCHAR(8), EndTime VARCHAR(8), \
                Room INT, Building VARCHAR(15), Quarter VARCHAR(6), Year INT, \
                PRIMARY KEY (CoursePrefix, CourseNumberPrefix, Number, Quarter, Year), FOREIGN KEY (CoursePrefix, CourseNumberPrefix) REFERENCES Course (Prefix, Number), FOREIGN KEY (Teacher) REFERENCES Teacher (Name) );"
                )

            cursor.commit()
            
            # Inserts into DB 
            # (probably needs to do a check later, and only update if already existent)
            insert_query = f"INSERT INTO Section VALUES ({sqlquote(self.course_prefix)} \
                , {sqlquote(self.course_number_prefix)}, {sqlquote(self.number)}  \
                , {sqlquote(self.teacher)}, {sqlquote(self.section_type)}  \
                , {sqlquote(self.days)}, {sqlquote(self.start_time)}  \
                , {sqlquote(self.end_time)}, {sqlquote(self.room)}  \
                , {sqlquote(self.building)}, {sqlquote(self.quarter)}  \
                , {sqlquote(self.year)}, {sqlquote(self.quarter)}  \
                )"

            cursor.execute(insert_query)
            cursor.commit()

class Teacher:
    '''Represents our Teacher table'''

    def __init__(self, name, room, building, phone, email, title, office_hours, how_to_connect):
        '''Creates a Teacher'''
        self.name = name
        self.room = room
        self.building = building
        self.phone = phone
        self.email = email
        self.title = title
        self.office_hours = office_hours
        self.how_to_connect = how_to_connect

    # inserts into DB
    def insert(self):
        '''Inserts Teacher into DB'''
        

def sqlquote(value):
    """Naive SQL quoting
    All values except NULL are returned as SQL strings in single quotes,
    with any embedded quotes doubled.
    """
    if value is None:
         return 'NULL'
    return "'{}'".format(str(value).replace("'", "''")) 