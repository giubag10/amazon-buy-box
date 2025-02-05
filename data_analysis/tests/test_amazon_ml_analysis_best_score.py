from unittest import TestCase

from parameterized import parameterized
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from data_analysis.scripts.amazon_ML_analysis import exec_ml_analysis_by_clf
from data_analysis.scripts.amazon_ML_constants import S_inputs, \
    L_inputs, XL_inputs, best_params_cart, best_params_random_forest, \
    best_params_svc, best_params_gradient_boosting, best_params_logistic_regression, best_params_mlp, best_params_knn, \
    feature_columns_opt
from data_analysis.scripts.amazon_data_normalizer import normalize_amazon_data
from data_analysis.scripts.amazon_data_reader import import_input_json_files_from_dir


# Da lanciare con workspace la cartella scripts
class Test(TestCase):

    @parameterized.expand([
        # CART
        [
            "CART", DecisionTreeClassifier(**best_params_cart[0]), S_inputs
        ],
        [
            "CART", DecisionTreeClassifier(**best_params_cart[1]), L_inputs
        ],
        [
            "CART", DecisionTreeClassifier(**best_params_cart[2]), XL_inputs
        ],
        # RANDOM FOREST
        [
            "RANDOM FOREST", RandomForestClassifier(**best_params_random_forest[0]), S_inputs
        ],
        [
            "RANDOM FOREST", RandomForestClassifier(**best_params_random_forest[1]), L_inputs
        ],
        [
            "RANDOM FOREST", RandomForestClassifier(**best_params_random_forest[2]), XL_inputs
        ],
        # SVC
        [
            "SVC", SVC(**best_params_svc[0]), S_inputs
        ],
        [
            "SVC", SVC(**best_params_svc[1]), L_inputs
        ],
        [
            "SVC", SVC(**best_params_svc[2]), XL_inputs
        ],
        # GRADIENT BOOSTING
        [
            "GRADIENT BOOSTING", GradientBoostingClassifier(**best_params_gradient_boosting[0]), S_inputs
        ],
        [
            "GRADIENT BOOSTING", GradientBoostingClassifier(**best_params_gradient_boosting[1]), L_inputs
        ],
        [
            "GRADIENT BOOSTING", GradientBoostingClassifier(**best_params_gradient_boosting[2]), XL_inputs
        ],
        # LOGISTIC REGRESSION
        [
            "LOGISTIC REGRESSION", LogisticRegression(**best_params_logistic_regression[0]), S_inputs
        ],
        [
            "LOGISTIC REGRESSION", LogisticRegression(**best_params_logistic_regression[1]), L_inputs
        ],
        [
            "LOGISTIC REGRESSION", LogisticRegression(**best_params_logistic_regression[2]), XL_inputs
        ],
        # MLP  # Aumenta le iterazioni per la convergenza
        [
            "MLP", MLPClassifier(**best_params_mlp[0]), S_inputs
        ],
        [
            "MLP", MLPClassifier(**best_params_mlp[1]), L_inputs
        ],
        [
            "MLP", MLPClassifier(**best_params_mlp[2]), XL_inputs
        ],
        # KNN
        [
            "KNN", KNeighborsClassifier(**best_params_knn[0]), S_inputs
        ],
        [
            "KNN", KNeighborsClassifier(**best_params_knn[1]), L_inputs
        ],
        [
            "KNN", KNeighborsClassifier(**best_params_knn[2]), XL_inputs
        ]
    ])
    def test_accuracy_ml_params(self, algorithm, clf, dir_path_test_files):
        amazon_data = import_input_json_files_from_dir(dir_path_test_files)
        normalized_data = normalize_amazon_data(amazon_data)
        print("Dataset size:", len(normalized_data))

        for test_size in [None, 0.1, 0.2]:
            perm_importance, accuracy = exec_ml_analysis_by_clf(clf, algorithm, normalized_data, test_size, feature_columns_opt)
            self.assertTrue(round(accuracy, 2) >= 0.95)

