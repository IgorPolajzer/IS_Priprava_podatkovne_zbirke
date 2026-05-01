| Št. | Algoritem (Razred) | Hiperparameter 1 | Hiperparameter 2 | Hiperparameter 3 |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **KNeighborsClassifier** | `n_neighbors`: [1, 5, 21] | `weights`: ['uniform', 'distance'] | `metric`: ['euclidean', 'manhattan'] |
| **2** | **LogisticRegression** | `C`: [0.01, 1.0, 100.0] | `penalty`: ['l2', None] | `solver`: ['lbfgs', 'saga'] |
| **3** | **DecisionTreeClassifier** | `max_depth`: [3, 10, None] | `criterion`: ['gini', 'entropy'] | `min_samples_leaf`: [1, 5, 20] |
| **4** | **RandomForestClassifier** | `n_estimators`: [10, 100] | `max_features`: ['sqrt', 'log2'] | `bootstrap`: [True, False] |
| **5** | **AdaBoostClassifier** | `n_estimators`: [50, 100] | `learning_rate`: [0.1, 1.0] | `algorithm`: ['SAMME', 'SAMME.R'] |
| **6** | **GaussianNB** | `var_smoothing`: [1e-9, 1e-5] | / | / |
| **7** | **LinearSVC** | `C`: [0.1, 1.0, 10.0] | `loss`: ['hinge', 'squared_hinge'] | `tol`: [1e-4, 1e-3] |
| **8** | **MLPClassifier** | `hidden_layer_sizes`: [(50,), (100, 50)] | `activation`: ['relu', 'tanh'] | `alpha`: [0.0001, 0.05] |
| **9** | **SGDClassifier** | `loss`: ['hinge', 'log_loss'] | `penalty`: ['l1', 'l2', 'elasticnet'] | `learning_rate`: ['constant', 'adaptive'] |
| **10** | **ExtraTreesClassifier** | `n_estimators`: [100, 200] | `max_depth`: [10, 20] | `min_samples_split`: [2, 10] |