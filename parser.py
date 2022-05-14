from urllib.request import urlopen
from bs4 import BeautifulSoup

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

    # inserts into DB
    def insert(self):
        '''Inserts Course into DB'''

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

CSC_CATALOG_LINK = "https://catalog.calpoly.edu/coursesaz/csc/"
STATS_CATALOG_LINK = "https://catalog.calpoly.edu/collegesandprograms/collegeofsciencemathematics/statistics/#courseinventory"