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

        '''
        for teacher names the tokens are going to be separate for first and last names so we need a way to match those.
        Potentially seperate them in 

        need to make sure everything in these lists are lowercase so they match in the mapping function
        '''

        # Teacher Variables
        self.teacher_names = self.getVariable("Name", "Teacher")
        self.teacher_titles = self.getVariable("Title", "Teacher")
        
        # Course Variables
        self.course_prefixes = self.getVariable("Prefix", "Course")
        self.course_numbers = self.getVariable("Number", "Course")
        self.course_titles = self.getVariable("Title", "Course")
        self.course_descs = self.getVariable("CourseDesc", "Course")

        # Section Variables

    '''
    input
    variables: special words (ie. "Paul Anderson", "building 192", "CSC 357")
    query_match: answer chosen by classifier (ie. ")

    output
    answer: the answer to the question originally asked in string form.
    '''
    def get_answer(self, variables: dict, query_match: str) -> str:
        split_q = query_match.split(" ")
        for i, tok in enumerate(split_q):
            try:
                var_match = variables[tok]
                split_q[i] = var_match
            except KeyError:
                if '[' in tok and ']' in tok:
                    raise Exception("uncaught variable:", tok)
        return " ".join(split_q)


    '''
    input
    usr_in: string from the user input

    output
    map: dictionary matching words to variables (ie. {'[CSSE-Faculty]':'Paul Anderson'})
    '''
    def key_word_map(self, tokens: list) -> dict:
        var_map = {}
        # variables = ['[CSSE-Faculty]','[STAT-Faculty]','[PREFIX]','[CourseNum]','[Course]','[CourseType]','[Section]','[Building]','[Room]','[Day]','[Time]','[Subject]','[Quarter]','[Year]','[Enrolled]','[Wait]','[Job-Title]']


        num_tok = len(tokens)
        for i, token in enumerate(tokens):
            token = token.lower()
            next_t = ""
            if (i + 1) < num_tok:
                next_t = tokens[i+1]
            name = token+" "+next_t
            if name in self.teacher_names: # need a way to distinguish between CSSE-Faculty and STAT=Faculty
                var_map['[CSSE-Faculty]'] = name
            elif token in self.teacher_titles:
                var_map['[Job-Title]'] = token
            elif token in self.course_prefixes:
                var_map['[PREFIX]'] = token
            elif token in self.course_numbers:
                var_map['[CourseNum]'] = token
            elif token in self.course_titles:
                var_map['[Course]'] = token
        return var_map
    
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

if __name__ == '__main__':
    main()

