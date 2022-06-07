from ast import keyword
from audioop import reverse
from lib2to3.pgen2 import token
import string
import pymysql
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

from models import Bagging, variables, corpus_training

class Tagger:
    def __init__(self):
        self.createClassifier()

        '''
        Still need to implement:
        [Subject] [Enrolled] [Wait] 

        How are we going to match Subject? "A subject phrase like "AI", "Linear Analysis" or "Operating Systems""
        enrolled and wait won't be in the search prompts right?
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
        self.course_types = ["lecture", "lab", "seminar"]

        # Section Variables

        # Miscellaneous
        self.days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        self.quarters = ["fall", "winter", "spring", "summer"]

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
        print(tokens)
        for i, token in enumerate(tokens):
            token = token.lower()
            # create possible two token tag (ie "Paul Anderson", "building 06", "section 5")
            next_t = ""
            if (i + 1) < len(tokens):
                next_t = tokens[i+1]
            two_tok = token+" "+next_t
            two_tok = two_tok.lower()
            # create possible PREFIX, CourseNum combo (ie "csc466" with no space)
            prefix = ""
            num = ""
            for char in token:
                if char.isdigit():
                    num += char
                else:
                    prefix += char
            # check for possible times
            time = ""
            if token == ":" and i > 0 and i < (len(tokens) - 1) and tokens[i-1].isdigit() and tokens[i+1][:2].isdigit():
                time = tokens[i-1] + token + tokens[i+1]
                if i < (len(tokens) - 2): 
                    if tokens[i+2].lower() == "am" or tokens[i+2].lower() == "pm":
                        time = time + " " + tokens[i+2]
                var_map['[Time]'] = time
                reverse_var_map[time] = '[Time]' 
            elif two_tok in [name.lower() for name in self.csse_teacher_names]:
                reverse_var_map[two_tok] = '[CSSE-Faculty]'
                name = two_tok.split(" ")
                name[0] = name[0][0].upper()+name[0][1:]
                name[1] = name[1][0].upper()+name[1][1:]
                name = " ".join(name)
                var_map['[CSSE-Faculty]'] = name
            elif two_tok in [name.lower() for name in self.stat_teacher_names]:
                reverse_var_map[two_tok] = '[STAT-Faculty]'
                name = two_tok.split(" ")
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
            elif token in self.course_types:
                var_map['[CourseType]'] = token
                reverse_var_map[token] = '[CourseType]'
            elif prefix in self.course_prefixes and num in self.course_numbers:
                var_map['[PREFIX]'] = prefix
                var_map['[CourseNum]'] = num
                reverse_var_map[token] = '[PREFIX][CourseNum]'
            elif two_tok.split(" ")[0] == 'section':
                s_num = two_tok.split(" ")[1]
                if s_num.isdigit():
                    if len(s_num) == 1:
                        s_num = "0"+s_num
                    var_map['[Section]'] = s_num
                    reverse_var_map[two_tok] = '[Section]'
            elif two_tok.split(" ")[0] == 'building':
                b_num = two_tok.split(" ")[1]
                if b_num.isdigit():
                    var_map['[Building]'] = b_num
                    reverse_var_map[two_tok] = '[Building]'
            elif two_tok.split(" ")[0] == 'room':
                r_num = two_tok.split(" ")[1]
                if r_num.isdigit():
                    var_map['[Room]'] = r_num
                    reverse_var_map[two_tok] = '[Room]'        
            elif token in self.days or token[:-1] in self.days:
                reverse_var_map[token] = '[Day]'
                if token[-1].lower() == "s":
                    token = token[:-1]
                var_map['[Day]'] = token
            elif token == "2021" or token == "2022":
                var_map['[Year]'] = token
                reverse_var_map[token] = '[Year]'
            elif token in self.quarters:
                var_map['[Quarter]'] = token
                reverse_var_map[token] = '[Quarter]'
        
        for course in self.course_titles:
            c_title = "".join(char for char in course if char.isalnum() or char == " ")
            course = "".join(char.lower() for char in c_title)
            if course.lower() in var_str:
                all_accounted_for = True
                for c in course.split(" "):
                    if c not in var_str.split(" "):
                        all_accounted_for = False
                if all_accounted_for:
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
            vars = executeSelect(f"""SELECT DISTINCT {variable} FROM {table}""")
        else:
            vars = executeSelect(f"""SELECT DISTINCT {variable} FROM {table} WHERE {whereVar} = "{whereVal}" """)

        return [str(var[0]).lower() for var in vars if var[0]]

    def predict(self, tokens):
        X_test = self.td.transform([" ".join(tokens)])
        return self.classifier.predict(X_test)[0]


def executeSelect(query):
    connection = pymysql.connect(
        user="jcavalca466",
        password="jcavalca466985",
        host="localhost",
        db="jcavalca466",
        # port=9090,  # comment out this if running on frank
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()
    return cursor.fetchall()

def main():
    first = True
    print("Welcome to CalPAss!")
    print("Please ask any questions you have. When you are done, type exit")
    tagger = Tagger()
    while True:
        if first:
            first = False
        else:
            print("\nAsk another question!")
        # Gets user input
        user_input = input()

        # Stop command
        if user_input.lower() == "exit":
            break

        # Tokenize input
        tokens = [token.lower() for token in wordpunct_tokenize(user_input)]
        
        #print(tokens, user_input)
        var_string, var_map = tagger.key_word_map(tokens, user_input)
        print(var_string, var_map)

        # Figure out intent
        intent_class = tagger.predict(var_string)
        print("intent class:",intent_class)

if __name__ == "__main__":
    main()
