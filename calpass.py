import string
import pymysql
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

from models import Bagging, variables, corpus_training

class Tagger:
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
        self.td = TfidfVectorizer(stop_words="english")
        y_train, X_train = zip(*corpus_training.items())

        # Combining example queries to feed one intent per document
        X_train = [" ".join(x) for x in X_train]
        
        # Removing variable names from testing data
        for var in variables:
            X_train = [x.replace(var, "") for x in X_train]

        # Tokenize and combine to strip punctuation
        X_train = [(" ".join(wordpunct_tokenize(x))).lower() for x in X_train]

        # Creating training data
        X_train = self.td.fit_transform(X_train).toarray()

        # Creates and fits a Naives Bayes Classifier
        self.classifier = Bagging()
        self.classifier.fit(X_train, y_train)

    def getVariable(self, variable, table):
        vars = executeSelect(f"""SELECT DISTINCT {variable} FROM {table}""")
        return [var[0] for var in vars]

    def predict(self, tokens):
        X_test = self.td.transform([" ".join(tokens)])
        return self.classifier.predict(X_test)[0]


def executeSelect(query):
    connection = pymysql.connect(
        user="jcavalca466",
        password="jcavalca466985",
        host="localhost",
        db="jcavalca466",
        port=9090,  # comment out this if running on frank
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

        # Gets user input
        user_input = input()

        # Stop command
        if user_input.lower() == "exit":
            break

        # Tokenize input
        tokens = [token.lower() for token in wordpunct_tokenize(user_input)]

        # Figure out intent
        intent_class = tagger.predict(tokens)

        print(tokens)
        print(intent_class)


if __name__ == "__main__":
    main()
