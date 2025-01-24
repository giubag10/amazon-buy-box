from unittest import TestCase

from parameterized import parameterized
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from data_analysis.scripts.amazon_ML_constants import param_grid_random_forest, S_inputs, \
    L_inputs, XL_inputs, target_features, param_grid_mlp, param_grid_knn, param_grid_gradient_boosting, \
    param_grid_logistic_regression, param_grid_svc, param_grid_cart, feature_columns_opt
from data_analysis.scripts.amazon_data_normalizer import normalize_amazon_data
from data_analysis.scripts.amazon_data_reader import import_input_json_files_from_dir


# Da lanciare con workspace la cartella tests mentre bisogna cambiare localmente gli import in data_analysis.scripts.*
# I migliori parametri vengono raccolti e testati nel file test_amazon_ml_analysis_best_score.py
class Test(TestCase):

    @parameterized.expand([
        # CART
        [
            DecisionTreeClassifier(), param_grid_cart, S_inputs
        ],
        [
            DecisionTreeClassifier(), param_grid_cart, L_inputs
        ],
        [
            DecisionTreeClassifier(), param_grid_cart, XL_inputs
        ],
        # RANDOM FOREST
        [
            RandomForestClassifier(), param_grid_random_forest, S_inputs
        ],
        [
            RandomForestClassifier(), param_grid_random_forest, L_inputs
        ],
        [
            RandomForestClassifier(), param_grid_random_forest, XL_inputs
        ],
        # SVC
        [
            SVC(), param_grid_svc, S_inputs
        ],
        [
            SVC(), param_grid_svc, L_inputs
        ],
        [
            SVC(), param_grid_svc, XL_inputs
        ],
        # GRADIENT BOOSTING
        [
            GradientBoostingClassifier(), param_grid_gradient_boosting, S_inputs
        ],
        [
            GradientBoostingClassifier(), param_grid_gradient_boosting, L_inputs
        ],
        [
            GradientBoostingClassifier(), param_grid_gradient_boosting, XL_inputs
        ],
        # LOGISTIC REGRESSION
        [
            LogisticRegression(), param_grid_logistic_regression, S_inputs
        ],
        [
            LogisticRegression(), param_grid_logistic_regression, L_inputs
        ],
        [
            LogisticRegression(), param_grid_logistic_regression, XL_inputs
        ],
        # MLP  # Aumenta le iterazioni per la convergenza
        [
            MLPClassifier(max_iter=500), param_grid_mlp, S_inputs
        ],
        [
            MLPClassifier(max_iter=500), param_grid_mlp, L_inputs
        ],
        [
            MLPClassifier(max_iter=500), param_grid_mlp, XL_inputs
        ],
        # KNN
        [
            KNeighborsClassifier(), param_grid_knn, S_inputs
        ],
        [
            KNeighborsClassifier(), param_grid_knn, L_inputs
        ],
        [
            KNeighborsClassifier(), param_grid_knn, XL_inputs
        ]
    ])
    def test_accuracy_ml_params(self, clf, param_grid, dir_path_test_files):
        amazon_data = import_input_json_files_from_dir(dir_path_test_files)
        normalized_data = normalize_amazon_data(amazon_data)
        print("Dataset size:", len(normalized_data))

        encoded_features = normalized_data[feature_columns_opt]
        encoded_target = normalized_data[target_features]

        # Esegui la ricerca grid
        grid_search = GridSearchCV(clf, param_grid, cv=5)
        grid_search.fit(encoded_features, encoded_target)

        # Stampa i migliori parametri
        print("Best Score:", grid_search.best_score_)
        print("Best Params:", grid_search.best_params_)

        self.assertTrue(round(grid_search.best_score_, 2) >= 0.95)
