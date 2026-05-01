import sys

from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from predictor.alphabet_data import AlphabetData

# Features -> x [][]
# Labels (a,b,c,d...) -> y []

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: python main.py <dataset_folder_path>")
        sys.exit()

    classifier = sys.argv[1]
    folder_path = sys.argv[2]

    alphabet_data = AlphabetData(folder_path)
    x_train, x_test, y_train, y_test = alphabet_data.get_train_test()

    clf = None
    if classifier == "-knn":
        clf = KNeighborsClassifier(n_neighbors=3, weights='distance')
    else:
        print("Incorrect classifier name")
        sys.exit()

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", clf),
    ])

    pipeline.fit(x_train, y_train)

    accuracy = pipeline.score(x_test, y_test)
    print(accuracy)





