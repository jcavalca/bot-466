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
    ],
    # Asks for building given a Professor.
    1: [
        "What building is [CSSE-Faculty] office hours?",
        "What is the office hours building for [CSSE-Faculty]?",
    ],
    # Asks for teachers given a class and quarter.
    2: [
        "Who teaches [PREFIX] [CourseNum] this quarter?",
        "Who is teaching [PREFIX] [CourseNum] on [Quarter]?",
    ],
    # Asks for classes given a professor and quarter.
    3: [
        "Which courses are [CSSE-Faculty] teaching this quarter?",
        "What classes are [CSSE-Faculty] teaching on [Quarter]?",
    ],
    # Asks for classes given a prefix and quarter.
    4: [
        "What [PREFIX] courses are offered this [Quarter]?",
        "In [Quarter], what [PREFIX] classes will be offered?",
    ],
    # Asks for classes given a prefix, start time and quarter.
    5: [
        "Which [PREFIX] courses start at 10AM this quarter?",
        "What [PREFIX] courses begin at 1PM on [Quarter]?",
    ],
    # Asks for classes given a prefix, end time and quarter.
    6: [
        "Which [PREFIX] courses end at 10AM this quarter?",
        "What [PREFIX] courses finish at 1PM on [Quarter]?",
    ],
    # Asks for office hours time given a professor.
    7: [
        "When can I go to [CSSE-Faculty] office?",
        "What time is [CSSE-Faculty] office hours?",
    ],
    # Asks for sections times given a class, type and quarter.
    8: [
        "What times are [PREFIX] [CourseNum] [CourseType] offered this quarter?",
        "When is [PREFIX] [CourseNum] [CourseType] offered on [Quarter]?",
    ],
    # Asks for pre requisites given a class.
    9: [
        "What are the pre requisites for [PREFIX] [CourseNum]?",
        "What do I need before taking [PREFIX] [CourseNum]",
    ],
    # Asks for units given a class.
    10: [
        "How many units is [PREFIX] [CourseNum]?",
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
        "What is [CSSE-Faculty]'s phone?",
    ],
    # Asks how to connect given a teacher.
    13: [
        "How can I connect to [CSSE-Faculty]?",
        "How can I reach [CSSE-Faculty]?",
    ],
    # Asks description given a course.
    14: [
        "How is the course [PREFIX] [CourseNum]?",
        "Describe for me [PREFIX] [CourseNum]?",
    ],
    # Asks number of section given a course and quarter.
    15: [
        "How many sections of [PREFIX] [CourseNum] are offered this quarter?",
        "In [Quarter], how many sections of [PREFIX] [CourseNum] will be offered?",
    ],
    # Asks room given a section.
    16: [
        "What's the room for [PREFIX][CourseNum]-[Section] this quarter",
    ],
    # Asks building given a section.
    17: [
        "What's the building for [PREFIX][CourseNum]-[Section] this quarter",
    ],
    # Asks teacher's job title
    18: [
        "What's the title of [CSSE-Faculty]?",
        "Give me the title for [CSSE-Faculty]?",
    ],
    # Asks type of section.
    19: [
        "What's the type of [PREFIX][CourseNum]-[Section]?",
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
