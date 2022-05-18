import string
import pymysql


class Tagger():
    def __init__(self) -> None:
        self.teacher_names = getTeacherNames()
        self.course_prefixes = getCoursePrefixes()
        self.course_numbers = getCourseNumbers()

    def tag(self, tokens) -> None:
       pass

def getCourseNumbers():
    numbers = executeSelect("SELECT DISTINCT Number FROM Course")
    return [number[0] for number in numbers]

def getCoursePrefixes():
    prefixes = executeSelect("SELECT DISTINCT Prefix FROM Course")
    return [prefix[0] for prefix in prefixes]

def getTeacherNames():
    names = executeSelect("SELECT Name FROM Teacher")
    return [name[0] for name in names]

def executeSelect(query):
    connection = pymysql.connect(
                user     = "jcavalca466",
                password = "jcavalca466985",
                host     = "localhost",
                db       = "jcavalca466",
                port     = 9090 # comment out this if running on frank
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()
    return cursor.fetchall()

def main():
    print("Welcome to CalPAss!")
    print("Please ask any questions you have. When you are done, type exit")
    tagger = Tagger()

    while True:

        # Strips spaces and punctuation
        user_input = input().strip().translate(str.maketrans('', '', string.punctuation))

        if user_input.lower() == "exit":
            break
        
        tokens = user_input.split()
        print(tagger.course_numbers)
        tags = tagger.tag(tokens)

if __name__ == '__main__':
    main()
