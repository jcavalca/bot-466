from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
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
    0: [
        "What's the room for [CSSE-Faculty] office hours?",
        "What room is [CSSE-Faculty] office hours?",
    ],
    1: [
        "What building is [CSSE-Faculty] office hours?",
        "What is the office hours building for [CSSE-Faculty]?",
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
            DecisionTreeClassifier(),
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
        print(preds)
        return majority_vote(preds)
