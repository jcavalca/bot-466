from bs4 import BeautifulSoup
from parser import Course
import requests
import pymysql
import re



CSC_CATALOG_LINK = "https://catalog.calpoly.edu/coursesaz/csc/"
STATS_CATALOG_LINK = "https://catalog.calpoly.edu/coursesaz/stat/"

csc_request = requests.get(CSC_CATALOG_LINK)
stat_request = requests.get(STATS_CATALOG_LINK)

csc_soup = BeautifulSoup(csc_request.text,"html.parser")
stat_soup = BeautifulSoup(stat_request.text, "html.parser")

courseDB = {}

for course in csc_soup.find_all('div', attrs={'class':'courseblock'}):
    nameHTML = course.find('p', attrs={'class':'courseblocktitle'})

    name = nameHTML.get_text().split("\n")[0].split()
    prefix = name[0]
    courseNum = name[1].replace(".","")
    title = " ".join(name[2:])
    units = nameHTML.get_text().split("\n")[1].split()[0]
    prereq = course.get_text().split("\n")[4].split(":")[1][1:]
    desc = course.find('div', attrs={'class':'courseblockdesc'}).get_text().split('\n')[1]
    course_object = Course(prefix, courseNum, title, units, prereq, desc)
    courseDB[prefix+courseNum] = course_object

for course in stat_soup.find_all('div', attrs={'class':'courseblock'}):
    nameHTML = course.find('p', attrs={'class':'courseblocktitle'})

    name = nameHTML.get_text().split("\n")[0].split()
    prefix = name[0]
    courseNum = name[1].replace(".","")
    title = " ".join(name[2:])
    units = nameHTML.get_text().split("\n")[1].split()[0]
    try:
        prereq = course.get_text().split("\n")[4].split(":")[1][1:]
    except IndexError:
        prereq = "None listed."
    desc = course.find('div', attrs={'class':'courseblockdesc'}).get_text().split('\n')[1]
    course_object = Course(prefix, courseNum, title, units, prereq, desc)
    courseDB[prefix+courseNum] = course_object

    
# for key in courseDB.keys():
#     print(courseDB[key])
#     print()
