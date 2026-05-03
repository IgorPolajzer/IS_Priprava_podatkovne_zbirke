import gc
import glob
import os
import sys
import cupy as cp
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import cuml.accel
cuml.accel.install()

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from predictor.alphabet_data import AlphabetData

RESULTS_DIR = "results_1-5"
RESULTS_FILE = f"{RESULTS_DIR}/results"

CONFIGS = [
    # LDA
    *[("-lda", s, t, "0")
      for s in ["svd", "lsqr", "eigen"]
      for t in ["1e-4", "1e-2"]],

    # Extra Trees
    *[("-etc", n, d, s)
      for n in ["10", "25"]
      for d in ["5", "10"]
      for s in ["2", "5"]],

    # Logistic Regression
    *[("-lr", c, p, a)
      for c in ["0.01", "1.0", "100.0"]
      for p in ["l2", "None"]
      for a in ["lbfgs", "saga"]],

    # k-NN
    *[("-knn", n, w, m)
      for n in ["1", "5", "21"]
      for w in ["uniform", "distance"]
      for m in ["euclidean", "manhattan"]],

    # Decision Tree
    *[("-dtc", d, c, l)
      for d in ["3", "10"]
      for c in ["gini", "entropy"]
      for l in ["1", "5", "20"]],

    # Random Forest
    *[("-rfc", n, f, b)
      for n in ["5", "10"]
      for f in ["sqrt", "log2"]
      for b in ["True", "False"]],

    # AdaBoost
    *[("-abc", n, r, d)
      for n in ["25", "50"]
      for r in ["0.1", "1.0"]
      for d in ["1", "2"]],

    # Gaussian NB
    *[("-gnb", v, "0", "0")
      for v in ["1e-9", "1e-5"]],

    # Linear SVC
    *[("-lsvc", c, l, t)
      for c in ["0.1", "1.0", "10.0"]
      for l in ["hinge", "squared_hinge"]
      for t in ["1e-4", "1e-3"]],

    # SGD
    *[("-sgd", l, p, r)
      for l in ["hinge", "log_loss"]
      for p in ["l1", "l2", "elasticnet"]
      for r in ["constant", "adaptive"]],
]

CONFIGS_QUICK = [
    ("-rfc",  "10",    "sqrt",          "True"),
    ("-knn",  "5",     "uniform",       "euclidean"),
    ("-lr",   "1.0",   "l2",            "saga"),
    ("-dtc",  "10",    "gini",          "1"),
    ("-abc",  "50",    "1.0",           "1"),
    ("-gnb",  "1e-9",  "0",             "0"),
    ("-lsvc", "1.0",   "squared_hinge", "1e-4"),
    ("-lda", "svd", "1e-4", "0"),
    ("-sgd",  "hinge", "l2",            "constant"),
    ("-etc",  "100",   "10",            "2"),
]


def build_clf(classifier, hp1, hp2, hp3):
    if classifier == "-knn":
        return KNeighborsClassifier(n_neighbors=int(hp1), weights=hp2, metric=hp3, n_jobs=-1)
    elif classifier == "-lr":
        penalty = None if hp2 == "None" else hp2
        return LogisticRegression(C=float(hp1), penalty=penalty, solver=hp3, max_iter=1000, n_jobs=-1)
    elif classifier == "-dtc":
        depth = None if hp1 == "None" else int(hp1)
        return DecisionTreeClassifier(max_depth=depth, criterion=hp2, min_samples_leaf=int(hp3))
    elif classifier == "-rfc":
        return RandomForestClassifier(n_estimators=int(hp1), max_features=hp2, bootstrap=(hp3 == "True"))
    elif classifier == "-abc":
        return AdaBoostClassifier(n_estimators=int(hp1), learning_rate=float(hp2), estimator=DecisionTreeClassifier(max_depth=int(hp3)))
    elif classifier == "-gnb":
        return GaussianNB(var_smoothing=float(hp1))
    elif classifier == "-lsvc":
        return LinearSVC(C=float(hp1), loss=hp2, tol=float(hp3), dual="auto")
    elif classifier == "-lda":
        return LinearDiscriminantAnalysis(solver=hp1, tol=float(hp2))
    elif classifier == "-sgd":
        return SGDClassifier(loss=hp1, penalty=hp2, learning_rate=hp3, eta0=0.01, n_jobs=-1)
    elif classifier == "-etc":
        return ExtraTreesClassifier(n_estimators=int(hp1), max_depth=int(hp2), min_samples_split=int(hp3), n_jobs=-1)
    return None


def log_to_file(message, classifier):
    print(message)
    with open(RESULTS_FILE + classifier + ".txt", "a") as f:
        f.write(message + "\n")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    files = sorted(glob.glob("data_set_2/*.csv"))

    os.makedirs(RESULTS_DIR, exist_ok=True)

    for file_path in files:
        print(f"\nDatoteka: {file_path}")
        alphabet_data = AlphabetData(file_path)
        x_train, x_test, y_train, y_test = alphabet_data.get_train_test()

        for classifier, hp1, hp2, hp3 in CONFIGS:
            try:
                clf = build_clf(classifier, hp1, hp2, hp3)

                pipeline = Pipeline([
                    ("scaler", StandardScaler()),
                    ("classifier", clf),
                ])

                log_to_file(f"--- Running {classifier} with [{hp1}, {hp2}, {hp3}] on {file_path} ---", classifier)
                pipeline.fit(x_train, y_train)
                accuracy = pipeline.score(x_test, y_test)

                log_to_file(f"Accuracy: {accuracy:.4f}", classifier)
                log_to_file("-" * 50, classifier)
            except Exception as e:
                log_to_file(f"ERROR: {classifier} [{hp1}, {hp2}, {hp3}] on {file_path}: {e}", classifier)
                log_to_file("-" * 50, classifier)
            finally:
                del clf, pipeline
                gc.collect()
                cp.get_default_memory_pool().free_all_blocks()

    print(f"\nTestiranje končano. Rezultati so v f{RESULTS_DIR}.")