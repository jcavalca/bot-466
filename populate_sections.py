from turtle import title
from bs4 import BeautifulSoup
from parser import Section
from numpy import number
import requests
import pymysql
import re


ACCEPTED_COURSE_PREFIXES= ["STAT", "CSC", "CPE"]
SECTIONS_LINK_CSM = "https://schedules.calpoly.edu/depts_76-CSM_"
SECTIONS_LINK_CENG = "https://schedules.calpoly.edu/depts_52-CENG_"

# current, last and next quarters
times = ["curr.htm", "last.htm", "next.htm"]
links = []

for link in [SECTIONS_LINK_CSM, SECTIONS_LINK_CENG]:
    for time in times:
        links.append(link+time)

links.append("https://schedules.calpoly.edu/depts_76-CSM_2228.htm") # Fall 2022
links.append("https://schedules.calpoly.edu/depts_52-CENG_2228.htm") # Fall 2022


def check_tag(element, tag):
    if element:
        find =  element.find(tag)
        if find:
            return find.text

def check_simple(element):
    if element:
        return element.text

# Section is valid if it has all the necessary attributes
def check_section(section, year, quarter, default_teacher):
    
    teacher = check_tag(section.find('td', attrs={'class':'personName'}), 'a')
    if not teacher:
        teacher = default_teacher
        if not teacher:
            return  None, teacher
    
    course = check_tag(section.find('td', attrs={'class':'courseName active'}), 'a')
    if not course:
        return  None, teacher
    course_prefix, course_number_prefix = course.split()
    if course_prefix not in ACCEPTED_COURSE_PREFIXES:
        return  None, teacher

    course_section = check_simple(section.find('td', attrs={'class':'courseSection active'}))
    if not course_section:
        return None, teacher
    
    
    course_type = check_tag(section.find('td', attrs={'class':'courseType'}), 'span')
    if not course_type:
        return None, teacher

    course_days = check_tag(section.find('td', attrs={'class':'courseDays'}), 'span')
    if not course_days:
        return  None, teacher

    start_time = check_simple(section.find('td', attrs={'class':'startTime'}))
    if not start_time:
        return  None, teacher
        
    end_time = check_simple(section.find('td', attrs={'class':'endTime'}))
    if not end_time:
        return  None, teacher
    
    location = check_tag(section.find('td', attrs={'class':'location'}), 'a')
    if not location:
        return  None, teacher
    try:
        building, room = location.split("-")
    except:
        return None, teacher

    section_object = Section(
        course_prefix=course_prefix.strip(), 
        course_number_prefix=course_number_prefix.strip(),
        number=course_section.strip(),
        teacher=teacher.strip(),
        section_type=course_type.strip(),
        days=course_days.strip(),
        start_time=start_time.strip(),
        end_time=end_time.strip(),
        room=room.strip(),
        building=building.strip(),
        quarter=quarter.strip(),
        year=year.strip(),
    )
    return section_object, teacher

def getQuarterYear(soup):

    seasons = ["Fall", "Winter", "Spring", "Summer"]
    for season in seasons:
        try:
            quarter, _, year = soup.find('span', attrs={'class':'term' + season}).text.split()
            break
        except:
            continue

    return quarter, year 

for link in links:
    request = requests.get(link)

    soup = BeautifulSoup(request.text,"html.parser")

    courseDB = {}
    print(link)

    quarter, year = getQuarterYear(soup)
    

    teacher = None
    
    for section in soup.find_all('tr'):
        
        section, teacher = check_section(section, year, quarter, teacher)
        if section:
            courseDB[section.course_prefix+section.course_number_prefix+f"-{section.number} {quarter}-{year}"] = section


for key in courseDB.keys():
    print(courseDB[key])
    courseDB[key].insert()
    print()