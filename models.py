from sklearn.naive_bayes import GaussianNB, CategoricalNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import resample

variables = [
    "[CSSE-Faculty]",
    "[STAT-Faculty]",
    "[PREFIX]",
    "[CourseNum]",
    "[Course]",
    "[CourseType]",
    "[Section]",
    "[Building]",
    "[Room]",
    "[Day]",
    "[Time]",
    "[Subject]",
    "[Quarter]",
    "[Year]",
    "[Enrolled]",
    "[Wait]",
    "[Job-Title]",
]

corpus_training = {
    # Asks for room given a Professor.
    0: [
        "What's the room for [CSSE-Faculty] office hours?",
        "What room is [CSSE-Faculty] office hours?",
        "What is the room for [CSSE-Faculty]'s office hours?",
        "Which room are [CSSE-Faculty]'s office hours held in?",
    ],
    # Asks for building given a Professor.
    1: [
        "What building is [CSSE-Faculty]'s office hours?",
        "What is the building for [CSSE-Faculty]'s office hours?",
        "Which building are [CSSE-Faculty]'s office hours held in?",
        "What is the office hours building for [CSSE-Faculty]?",
    ],
    # Asks for teachers given a class and quarter.
    2: [
        "Who teaches [PREFIX] [CourseNum] this quarter?",
        "Who is teaching [PREFIX] [CourseNum] on [Quarter]?",
        "Who's teaching [PREFIX] [CourseNum] [Quarter] quarter?",
        "Who is the professor for [PREFIX] [CourseNum] [Quarter] quarter?",
        "Who is the instructor for [PREFIX] [CourseNum] [Quarter] quarter?",
    ],
    # Asks for classes given a professor and quarter.
    3: [
        "Which courses are [CSSE-Faculty] teaching this quarter?",
        "What courses are [CSSE-Faculty] teaching [Quarter] quarter?",
        "What classes are [CSSE-Faculty] teaching [Quarter] quarter?",
    ],
    # Asks for classes given a prefix and quarter.
    4: [
        "What [PREFIX] courses are offered this [Quarter]?",
        "What [PREFIX] courses are taught this [Quarter]?",
        "Which [PREFIX] courses are taught this [Quarter]?",
        "Which [PREFIX] courses are expected to be offered [Quarter] quarter?",
        "In [Quarter], what [PREFIX] classes will be offered?",
    ],
    # Asks for classes given a prefix, start time and quarter.
    5: [
        "Which [PREFIX] courses start at 10AM this quarter?",
        "What [PREFIX] courses start at 10AM [Quarter] quarter?",
        "What [PREFIX] courses begin at 1PM [Quarter] quarter?",
        "Which [PREFIX] courses begin at 1PM this quarter?",
    ],
    # Asks for classes given a prefix, end time and quarter.
    6: [
        "Which [PREFIX] courses end at 10AM this quarter?",
        "What [PREFIX] courses end at 10AM [Quarter] quarter?",
        "What [PREFIX] courses finish at 1PM on [Quarter]?",
        "Which [PREFIX] courses finish at 1PM this quarter?",
    ],
    # Asks for office hours time given a professor.
    7: [
        "When can I go to [CSSE-Faculty]'s office?",
        "What time is [CSSE-Faculty]'s office hours?",
        "When are [CSSE-Faculty]'s office hours?",
        "What are [CSSE-Faculty]'s office hours?",
        "What are the office hours for [CSSE-Faculty]?"
    ],
    # Asks for sections times given a class, type and quarter.
    8: [
        "What times are [PREFIX] [CourseNum] [CourseType] offered this quarter?",
        "What times are [PREFIX] [CourseNum] [CourseType] taught this quarter?",
        "What times does [PREFIX] [CourseNum] [CourseType] meet [Quarter] quarter?",
        "What time is [PREFIX] [CourseNum] [CourseType] offered this quarter?",
        "When is [PREFIX] [CourseNum] [CourseType] offered [Quarter] quarter?",
        "When is [PREFIX] [CourseNum] [CourseType] taught [Quarter] quarter?",
        "When does [PREFIX] [CourseNum] [CourseType] meet this quarter?",
    ],
    # Asks for pre requisites given a class.
    9: [
        "What are the pre requisites for [PREFIX] [CourseNum]?",
        "What are the prerequisites for [PREFIX] [CourseNum]?",
        "What do I need before taking [PREFIX] [CourseNum]",
    ],
    # Asks for units given a class.
    10: [
        "How many units is [PREFIX] [CourseNum]?",
        "How many units is [PREFIX] [CourseNum] worth?",
        "How many credits do I get for [PREFIX] [CourseNum]?",
    ],
    # Asks for a teacher email given a teacher.
    11: [
        "What is the email for [CSSE-Faculty]?",
        "What is [CSSE-Faculty]'s email?",
    ],
    # Asks for a teacher phone given a teacher.
    12: [
        "What is the phone for [CSSE-Faculty]?",
        "What is the phone number for [CSSE-Faculty]?",
        "What is [CSSE-Faculty]'s phone?",
        "What is [CSSE-Faculty]'s phone number?",
    ],
    # Asks how to connect given a teacher.
    13: [
        "How can I connect to [CSSE-Faculty]?",
        "How can I reach [CSSE-Faculty]?",
        "How can I contact [CSSE-Faculty]?",
        "How can I meet with [CSSE-Faculty]?",
    ],
    # Asks description given a course.
    14: [
        "How is the course [PREFIX] [CourseNum]?",
        "What is [PREFIX] [CourseNum]?",
        "Describe for me [PREFIX] [CourseNum]?",
    ],
    # Asks number of section given a course and quarter.
    15: [
        "How many sections of [PREFIX] [CourseNum] are offered this quarter?",
        "How many sections of [PREFIX] [CourseNum] are offered [Quarter] quarter?",
        "In [Quarter], how many sections of [PREFIX] [CourseNum] will be offered?",
    ],
    # Asks room given a section.
    16: [
        "What's the room for [PREFIX][CourseNum]-[Section] this quarter",
        "What's the room for [PREFIX][CourseNum] section [Section] this quarter",
        "Which room does [PREFIX][CourseNum]-[Section] meet in [Quarter] quarter?",
        "Which room is [PREFIX][CourseNum]-[Section] taught in [Quarter] quarter?",
    ],
    # Asks building given a section.
    17: [
        "What's the building for [PREFIX][CourseNum]-[Section] this quarter",
        "What's the building for [PREFIX][CourseNum] section [Section] this quarter",
        "Which building does [PREFIX][CourseNum]-[Section] meet in [Quarter] quarter?",
        "Which building is [PREFIX][CourseNum]-[Section] taught in [Quarter] quarter?",
    ],
    # Asks teacher's job title
    18: [
        "What's the title of [CSSE-Faculty]?",
        "What's the job title of [CSSE-Faculty]?",
        "Give me the title for [CSSE-Faculty]?",
        "Give me the job title for [CSSE-Faculty]?",
    ],
    # Asks type of section.
    19: [
        "What's the type of [PREFIX][CourseNum]-[Section]?",
        "What type of class is [PREFIX][CourseNum]-[Section]?",
        "What type of class is [PREFIX][CourseNum] section [Section]?",
        "Is [PREFIX][CourseNum]-[Section] a lecture, a lab, or a seminar?",

    ],
}

# Gets most frequent element of list
def most_frequent(L):
    return max(set(L), key=L.count)


# Performs majority vote on a set of predictions
def majority_vote(preds):
    final_preds = []
    for i in range(len(preds[0])):
        options = []
        for pred in preds:
            options.append(pred[i])

        final = most_frequent(options)
        final_preds.append(final)
    return final_preds


# Bagging Algo
class Bagging:
    def __init__(
        self,
        clfs=[
            GaussianNB(),
            CategoricalNB(min_categories=2),
            KNeighborsClassifier(n_neighbors=len(corpus_training)),
        ],
    ):
        self.clfs = clfs

    # Fits all Models, using bootstrap resampling
    def fit(self, train_points, train_labels):
        for clf in self.clfs:
            train_x_rep, train_y_rep = resample(train_points, train_labels)
            clf.fit(train_x_rep, train_y_rep)

    # Predicts w/ all Models, and final prediction is majority vote
    def predict(self, test_x):
        preds = []
        for clf in self.clfs:
            preds.append(clf.predict(test_x.toarray()))
        
        final_choice = majority_vote(preds)
        
        preds = [p[0] for p in preds]
        
        # If all models disagree, choose GaussianNB
        print(preds, final_choice)
        if preds.count(final_choice) == 1:
            return [preds[0]]

        return final_choice
