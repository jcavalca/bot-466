import string
import pymysql

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB


corpus = {
"What's the room for Fooad's office hours?":0,
"What room is Paul Anderson office hours?":0,
"What building is Paul Anderson office hours?" : 1,
"What is the office hours building for Paul Anderson?" : 1,
} 

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
        td = TfidfVectorizer(stop_words='english')
        X_train, y_train = zip(*corpus.items())
        X_train = td.fit_transform(X_train).toarray()
        classifier = BernoulliNB()
        classifier.fit(X_train, y_train)

        X_test = td.transform([' '.join(tokens)])
        print(classifier.predict(X_test))


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

        # Stop command
        if user_input.lower() == "exit":
            break
        
        # Tokenize input
        tokens = user_input.split()

        print(tokens)
        tags = tagger.tag(tokens)

if __name__ == '__main__':
    main()
