import string
import pymysql

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB


corpus_training = {
0: ["What's the room for Fooad's office hours?", "What room is Paul Anderson office hours?"],
1: ["What building is Paul Anderson office hours?", "What is the office hours building for Paul Anderson?"],
} 

class Tagger():
    def __init__(self):
        self.createClassifier()

        # Teacher Variables
        self.teacher_names = self.getVariable("Name", "Teacher")
        self.teacher_titles = self.getVariable("Title", "Teacher")
        
        # Course Variables
        self.course_prefixes = self.getVariable("Prefix", "Course")
        self.course_numbers = self.getVariable("Number", "Course")
        self.course_titles = self.getVariable("Title", "Course")
        self.course_descs = self.getVariable("CourseDesc", "Course")

        # Section Variables
    
    def createClassifier(self):
        # Perform TF-IDF on corpus
        self.td = TfidfVectorizer(stop_words='english')
        y_train, X_train = zip(*corpus_training.items())

        # combining example queries to feed one intent per document
        X_train = [' '.join(x) for x in X_train]

        X_train = self.td.fit_transform(X_train).toarray()

        # Creates and fits a Naives Bayes Classifier
        self.classifier = BernoulliNB()
        self.classifier.fit(X_train, y_train)

    def getVariable(self, variable, table):
        vars = executeSelect(f"""SELECT DISTINCT {variable} FROM {table}""")
        return [var[0] for var in vars]

    def predict(self, tokens):
        X_test = self.td.transform([' '.join(tokens)])
        return self.classifier.predict(X_test)[0]


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

        # Figure out intent
        intent_class = tagger.predict(tokens)

        print(tokens)
        print(intent_class)

if __name__ == '__main__':
    main()

