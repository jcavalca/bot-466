import string
import pymysql
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

import db
from models import Bagging, variables, corpus_training
import fetch_answer as fa

class Tagger:
    def __init__(self):
        self.createClassifier()

        '''
        for teacher names the tokens are going to be separate for first and last names so we need a way to match those.
        Potentially seperate them in 

        need to make sure everything in these lists are lowercase so they match in the mapping function
        '''

        # Teacher Variables
        self.all_teacher_names = self.getVariable("Name", "Teacher")
        self.stat_teacher_names = self.getVariable("Name", "Teacher", "Department", "STAT")
        self.csse_teacher_names = self.getVariable("Name", "Teacher", "Department", "CSSE")
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
    tokens: tokenized input string
    usr_in: original string from the user input

    output
    map: dictionary matching words to variables (ie. {'[CSSE-Faculty]':'Paul Anderson'})
    '''
    def key_word_map(self, tokens: list, usr_in: string):
        var_map = {}
        reverse_var_map = {}
        var_str = "".join(list(char.lower() for char in usr_in))
        for i, token in enumerate(tokens):
            token = token.lower()
            # create possible name (ie "Paul Anderson" with a space)
            next_t = ""
            if (i + 1) < len(tokens):
                next_t = tokens[i+1]
            name = token+" "+next_t
            # create possible PREFIX, CourseNum combo (ie "csc466" with no space)
            prefix = ""
            num = ""
            for char in token:
                if char.isdigit:
                    num += char
                else:
                    prefix += char
            if name in [name.lower() for name in self.csse_teacher_names]:
                reverse_var_map[name] = '[CSSE-Faculty]'
                name = name.split(" ")
                name[0] = name[0][0].upper()+name[0][1:]
                name[1] = name[1][0].upper()+name[1][1:]
                name = " ".join(name)
                var_map['[CSSE-Faculty]'] = name
            elif name in self.csse_teacher_names:
                reverse_var_map[name] = '[STAT-Faculty]'
                name = name.split(" ")
                name[0] = name[0][0].upper()+name[0][1:]
                name[1] = name[1][0].upper()+name[1][1:]
                name = " ".join(name)
                var_map['[STAT-Faculty]'] = name
            elif token in self.teacher_titles:
                var_map['[Job-Title]'] = token
                reverse_var_map[token] = '[Job-Title]'
            elif token in self.course_prefixes:
                var_map['[PREFIX]'] = token
                reverse_var_map[token] = '[PREFIX]'
            elif token in self.course_numbers:
                var_map['[CourseNum]'] = token
                reverse_var_map[token] = '[CourseNum]'
            elif token in self.course_titles:
                var_map['[Course]'] = token
                reverse_var_map[token] = '[Course]'
            elif prefix in self.course_prefixes and num in self.course_numbers:
                var_map['[PREFIX]'] = prefix
                var_map['CourseNum'] = num
                reverse_var_map[token] = '[PREFIX][CourseNum]'
        
        for course in self.course_titles:
            c_title = "".join(char for char in course if char.isalnum() or char == " ")
            course = "".join(char.lower() for char in c_title)
            if course.lower() in var_str:
                var_map['[Course]'] = c_title
                reverse_var_map[course] = '[Course]'

        for tok in reverse_var_map.keys():
            var_str = var_str.replace(tok, reverse_var_map[tok])

        return var_str, var_map
    
    def createClassifier(self):
        # Perform TF-IDF on corpus
        self.td = TfidfVectorizer(stop_words="english")
        y_train, X_train = zip(*corpus_training.items())

        # Combining example queries to feed one intent per document
        X_train = [" ".join(x) for x in X_train]
        
        # Tokenize and combine to strip punctuation
        X_train = [(" ".join(wordpunct_tokenize(x))).lower() for x in X_train]

        # Creating training data
        X_train = self.td.fit_transform(X_train).toarray()

        # Creates and fits a Naives Bayes Classifier
        self.classifier = Bagging()
        self.classifier.fit(X_train, y_train)

    def getVariable(self, variable, table, whereVar=None, whereVal=None):
        if whereVar is None and whereVal is None:
            vars = db.executeSelect(f"""SELECT DISTINCT {variable} FROM {table}""")
        else:
            vars = db.executeSelect(f"""SELECT DISTINCT {variable} FROM {table} WHERE {whereVar} = "{whereVal}" """)

        return [str(var[0]).lower() for var in vars if var[0]]

    def predict(self, tokens):
        X_test = self.td.transform([" ".join(tokens)])
        return self.classifier.predict(X_test)[0]



def main():
    print("Welcome to CalPass!")
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
        
        var_string, var_map = tagger.key_word_map(tokens, user_input)

        tokens = var_string.split()

        # Figure out intent
        intent_class = tagger.predict(tokens)
        
        # Return answer
        if intent_class in [0, 1, 7, 11, 12, 13, 18]:
            fa.fetch_teacher_answer(var_map, intent_class)
        if intent_class in [2, 3, 4, 5, 6, 8, 15, 16, 17, 19]:
            fa.fetch_section_answer(var_map, intent_class)
        if intent_class in [9, 10, 14]:
            fa.fetch_course_answer(var_map, intent_class)

if __name__ == "__main__":
    main()
