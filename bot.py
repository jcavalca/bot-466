import string
import pymysql


class Tagger():
    def __init__(self):
        # Teacher Variables
        self.teacher_names = self.getVariable("Name", "Teacher")
        self.teacher_titles = self.getVariable("Title", "Teacher")
        
        # Course Variables
        self.course_prefixes = self.getVariable("Prefix", "Course")
        self.course_numbers = self.getVariable("Number", "Course")
        self.course_titles = self.getVariable("Title", "Course")
        self.course_descs = self.getVariable("CourseDesc", "Course")

        # Section Variables

    def getVariable(self, variable, table):
        vars = executeSelect(f"""SELECT DISTINCT {variable} FROM {table}""")
        return [var[0] for var in vars]

    def tag(self, tokens):
       pass

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
        tags = tagger.tag(tokens)

if __name__ == '__main__':
    main()
