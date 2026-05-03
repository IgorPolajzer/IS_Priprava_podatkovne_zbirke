import sys

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from predictor.alphabet_data import AlphabetData

RESULTS_FILE = "results_1-10.txt"

def log_result(message):
    print(message)
    with open(RESULTS_FILE, "a") as f:
        f.write(message + "\n")


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("Usage: python main.py <classifier> <hp1> <hp2> <hp3> <dataset_folder_path>")
        print("Example: python main.py -knn 5 distance euclidean data_set/characteristics_1_1.csv")
        sys.exit()

    classifier = sys.argv[1]
    hp1 = sys.argv[2]
    hp2 = sys.argv[3]
    hp3 = sys.argv[4]
    folder_path = sys.argv[5]

    alphabet_data = AlphabetData(folder_path)
    x_train, x_test, y_train, y_test = alphabet_data.get_train_test()

    clf = None
    try:
        if classifier == "-knn":
            clf = KNeighborsClassifier(n_neighbors=int(hp1), weights=hp2, metric=hp3, n_jobs=-1)
        elif classifier == "-lr":
            penalty = None if hp2 == "None" else hp2
            clf = LogisticRegression(C=float(hp1), penalty=penalty, solver=hp3, max_iter=1000, n_jobs=-1)
        elif classifier == "-dtc":
            depth = None if hp1 == "None" else int(hp1)
            clf = DecisionTreeClassifier(max_depth=depth, criterion=hp2, min_samples_leaf=int(hp3))
        elif classifier == "-rfc":
            clf = RandomForestClassifier(n_estimators=int(hp1), max_features=hp2, bootstrap=(hp3 == "True"), n_jobs=-1)
        elif classifier == "-abc":
            clf = AdaBoostClassifier(n_estimators=int(hp1), learning_rate=float(hp2), estimator=DecisionTreeClassifier(max_depth=int(hp3)))
        elif classifier == "-gnb":
            clf = GaussianNB(var_smoothing=float(hp1))
        elif classifier == "-lsvc":
            clf = LinearSVC(C=float(hp1), loss=hp2, tol=float(hp3), dual="auto")
        elif classifier == "-mlp":
            # hp1 pričakuje "50" ali "100,50" -> pretvorba v tuple
            layers = tuple(map(int, hp1.split(',')))
            clf = MLPClassifier(hidden_layer_sizes=layers, activation=hp2, alpha=float(hp3), max_iter=500)
        elif classifier == "-sgd":
            clf = SGDClassifier(loss=hp1, penalty=hp2, learning_rate=hp3, eta0=0.01, n_jobs=-1)
        elif classifier == "-etc":
            clf = ExtraTreesClassifier(n_estimators=int(hp1), max_depth=int(hp2), min_samples_split=int(hp3), n_jobs=-1)
        else:
            print(f"Incorrect classifier name: {classifier}")
            sys.exit()

    except Exception as e:
        print(f"Error setting up classifier: {e}")
        sys.exit()

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", clf),
    ])

    log_result(f"--- Running {classifier} with [{hp1}, {hp2}, {hp3}] on {folder_path} ---")

    pipeline.fit(x_train, y_train)
    accuracy = pipeline.score(x_test, y_test)

    log_result(f"Accuracy: {accuracy:.4f}")
    log_result("-" * 50)