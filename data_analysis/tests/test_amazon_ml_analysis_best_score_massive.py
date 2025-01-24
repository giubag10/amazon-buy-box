from unittest import TestCase

from parameterized import parameterized
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from data_analysis.scripts.amazon_ML_analysis import exec_ml_analysis_by_clf
from data_analysis.scripts.amazon_data_normalizer import normalize_amazon_data
from data_analysis.scripts.amazon_data_reader import import_input_json_files_from_dir
from data_analysis.scripts.amazon_ML_constants import S_inputs, \
    L_inputs, XL_inputs, best_params_cart, best_params_random_forest, \
    best_params_svc, best_params_gradient_boosting, best_params_logistic_regression, best_params_mlp, best_params_knn, \
    feature_columns_opt


# Da lanciare con workspace la cartella tests mentre bisogna cambiare localmente gli import in data_analysis.scripts.*
class Test(TestCase):

    @parameterized.expand([
        # CART
        [
            "CART", DecisionTreeClassifier(**best_params_cart[0])
        ],
        [
            "CART", DecisionTreeClassifier(**best_params_cart[1])
        ],
        [
            "CART", DecisionTreeClassifier(**best_params_cart[2])
        ],
        # RANDOM FOREST
        [
            "RANDOM FOREST", RandomForestClassifier(**best_params_random_forest[0])
        ],
        [
            "RANDOM FOREST", RandomForestClassifier(**best_params_random_forest[1])
        ],
        [
            "RANDOM FOREST", RandomForestClassifier(**best_params_random_forest[2])
        ],
        # SVC
        [
            "SVC", SVC(**best_params_svc[0])
        ],
        [
            "SVC", SVC(**best_params_svc[1])
        ],
        [
            "SVC", SVC(**best_params_svc[2])
        ],
        # GRADIENT BOOSTING
        [
            "GRADIENT BOOSTING", GradientBoostingClassifier(**best_params_gradient_boosting[0])
        ],
        [
            "GRADIENT BOOSTING", GradientBoostingClassifier(**best_params_gradient_boosting[1])
        ],
        [
            "GRADIENT BOOSTING", GradientBoostingClassifier(**best_params_gradient_boosting[2])
        ],
        # LOGISTIC REGRESSION
        [
            "LOGISTIC REGRESSION", LogisticRegression(**best_params_logistic_regression[0])
        ],
        [
            "LOGISTIC REGRESSION", LogisticRegression(**best_params_logistic_regression[1])
        ],
        [
            "LOGISTIC REGRESSION", LogisticRegression(**best_params_logistic_regression[2])
        ],
        # MLP  # Aumenta le iterazioni per la convergenza
        [
            "MLP", MLPClassifier(**best_params_mlp[0])
        ],
        [
            "MLP", MLPClassifier(**best_params_mlp[1])
        ],
        [
            "MLP", MLPClassifier(**best_params_mlp[2])
        ],
        # KNN
        [
            "KNN", KNeighborsClassifier(**best_params_knn[0])
        ],
        [
            "KNN", KNeighborsClassifier(**best_params_knn[1])
        ],
        [
            "KNN", KNeighborsClassifier(**best_params_knn[2])
        ]
    ])
    def test_accuracy_ml_params(self, algorithm, clf):
        accuracy_total = 0
        test_num = 0
        for dir_path_test_files in [S_inputs, L_inputs, XL_inputs]:
            amazon_data = import_input_json_files_from_dir(dir_path_test_files)
            normalized_data = normalize_amazon_data(amazon_data)
            print("Dataset size:", len(normalized_data))

            for test_size in [None, 0.1, 0.2]:
                perm_importance, accuracy = exec_ml_analysis_by_clf(clf, algorithm, normalized_data, test_size, feature_columns_opt)
                accuracy_total = accuracy_total + accuracy
                test_num = test_num + 1

        accuracy_avg = accuracy_total/test_num
        print("Accuracy Average:", accuracy_avg)
        self.assertTrue(round(accuracy_avg, 2) >= 0.95)

