from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier, Perceptron
from sklearn.model_selection import StratifiedKFold, RepeatedKFold, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier

# Features
features = ["price_no_shipping", "total_price", "price_diff_prod", "price_diff",
            "shipping_price", "delivery_days", "price_diff_ship", "ratings_num",
            "ratings_avg", "ratings_perc_positive", "fba", "amazon", "new"]

# Target
target_features = ["buybox"]

# Opzione completa
feature_columns_opt = ["price_diff_prod", "price_diff", "price_diff_ship", "delivery_days", "ratings_num",
                       "ratings_avg", "ratings_perc_positive", "fba", "amazon", "new"]

# Utile ai test: path verso input di dimesioni diverse
S_inputs = "../inputs/small"  # 7 gg di campioni
L_inputs = "../inputs/large"  # 20 gg di campioni
XL_inputs = "../inputs/extralarge"  # 38 gg di campioni

# ML algorithms
cart_alg_name = "CLASSIFICATION AND REGRESSION TREE"  # Classification And Regression Tree
random_forest_alg_name = "RANDOM FOREST"  # Random Forest
svm_alg_name = "SUPPORT VECTOR MACHINES"  # Support Vector Machines
gradient_boosting_alg_name = "GRADIENT BOOSTING"  # Gradient Boosting
logistic_regression_alg_name = "LOGISTIC REGRESSION"  # Logistic Regression
neural_network_alg_name = "MULTI-LAYER PERCEPTRON"  # Neural Network: Multi-Layer Perceptron
k_nearest_neighbors_alg_name = "K-NEAREST NEIGHBORS"  # K-Nearest Neighbors
all_algorithms = "ALL ALGORITHMS"  # All Algorithms

# Mappe degli iperparametri degli algoritmi di Machine Learning
param_grid_cart = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_leaf_nodes': [None, 5, 10, 15]
}
param_grid_random_forest = {
    'n_estimators': [100, 200, 500],  # Numero di alberi decisionali
    'max_depth': [None, 5, 10],  # Profondità massima degli alberi
    'min_samples_split': [2, 5],  # Minimo di campioni per splittare un nodo
    'min_samples_leaf': [1, 2]  # Minimo di campioni per essere una foglia
}
param_grid_svc = {
    'C': [0.1, 1, 10],  # Parametro di regolarizzazione
    'kernel': ['linear', 'rbf', 'poly'],  # Tipo di kernel
    'gamma': ['scale', 'auto'],  # Parametro per i kernel RBF e Poly
    'degree': [2, 3]  # Grado del polinomio per il kernel Poly
}
param_grid_gradient_boosting = {
    'n_estimators': [100, 200, 500],  # Numero di stimatori (alberi decisionali)
    'learning_rate': [0.1, 0.05, 0.01],  # Tasso di apprendimento
    'max_depth': [3, 5, 7],  # Profondità massima degli alberi
    'min_samples_split': [2, 5, 10],  # Minimo di campioni per splittare un nodo
    'min_samples_leaf': [1, 2, 4],  # Minimo di campioni per essere una foglia
}
param_grid_logistic_regression = param_grid = {
    'solver': ['liblinear', 'lbfgs', 'newton-cg', 'sag'],  # Specifica l'algoritmo di ottimizzazione da utilizzare
    'penalty': ['l1', 'l2', 'elasticnet'],  # Tipo di regolarizzazione
    'C': [0.001, 0.01, 0.1, 1, 10],  # Inverso del parametro di regolarizzazione
    'max_iter': [100, 500, 1000],  # Numero massimo di iterazioni per la convergenza
    'class_weight': [{0: 1, 1: 1}, {0: 1, 1: 2}, {0: 1, 1: 5}],  # Permette di assegnare pesi diversi alle classi, utile quando le classi sono sbilanciate
    'multi_class': ['ovr', 'multinomial']  # Strategia per la classificazione multi-classe
}
param_grid_mlp = {
    'hidden_layer_sizes': [(100,), (50, 50)],  # Numero di neuroni per strato nascosto
    'activation': ['relu', 'tanh'],  # Funzione di attivazione
    'solver': ['adam', 'sgd'],  # Ottimizzatore
    'alpha': [0.0001, 0.001],  # L2 regularization term
    'learning_rate': ['constant', 'adaptive']  # Tasso di apprendimento
}
param_grid_knn = {
    'n_neighbors': [3, 5, 7],  # Numero di vicini
    'weights': ['uniform', 'distance'],  # Ponderazione dei vicini
    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],  # Algoritmo per la ricerca dei vicini
    'p': [1, 2]  # Potenza della metrica di distanza (1: Manhattan, 2: Euclidea)
}


# Iperparametri degli algoritmi (scelti sulla base dell'esito dei test in test_amazon_ml_analysis_hyperparameters.py
best_params_cart = [
    {'criterion': 'entropy', 'max_depth': None, 'max_leaf_nodes': None, 'min_samples_leaf': 4, 'min_samples_split': 2, 'splitter': 'random'},  # Best for S
    {'criterion': 'entropy', 'max_depth': 20, 'max_leaf_nodes': None, 'min_samples_leaf': 4, 'min_samples_split': 10, 'splitter': 'random'},  # Best for L
    {'criterion': 'gini', 'max_depth': 15, 'max_leaf_nodes': None, 'min_samples_leaf': 4, 'min_samples_split': 2, 'splitter': 'random'}  # Best for XL
]
best_params_random_forest = [
    {'max_depth': 10, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 200},  # Best for S
    {'max_depth': 5, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 5, 'n_estimators': 100},  # Best for L
    {'max_depth': 10, 'max_features': 'sqrt', 'min_samples_leaf': 2, 'min_samples_split': 5, 'n_estimators': 500}  # Best for XL
]
best_params_svc = [
    {'C': 1, 'degree': 2, 'gamma': 'scale', 'kernel': 'rbf'},  # Best for S
    {'C': 1, 'degree': 2, 'gamma': 'scale', 'kernel': 'rbf'},  # Best for L
    {'C': 10, 'degree': 2, 'gamma': 'auto', 'kernel': 'poly'}  # Best for XL
]
best_params_gradient_boosting = [
    {'learning_rate': 0.1, 'max_depth': 3, 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 500},  # Best for S
    {'learning_rate': 0.01, 'max_depth': 7, 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 100},  # Best for L
    {'learning_rate': 0.05, 'max_depth': 7, 'min_samples_leaf': 2, 'min_samples_split': 2, 'n_estimators': 500}  # Best for XL
]
best_params_logistic_regression = [
    {'C': 1, 'class_weight': {0: 1, 1: 1}, 'max_iter': 100, 'multi_class': 'multinomial', 'penalty': 'l2', 'solver': 'newton-cg'},  # Best for S
    {'C': 0.1, 'class_weight': {0: 1, 1: 1}, 'max_iter': 100, 'multi_class': 'ovr', 'penalty': 'l2', 'solver': 'liblinear'},  # Best for L
    {'C': 10, 'class_weight': {0: 1, 1: 1}, 'max_iter': 100, 'multi_class': 'ovr', 'penalty': 'l2', 'solver': 'lbfgs'}  # Best for XL
]
best_params_mlp = [
    {'activation': 'relu', 'alpha': 0.0001, 'hidden_layer_sizes': (50, 50), 'learning_rate': 'adaptive', 'solver': 'adam'},  # Best for S
    {'activation': 'relu', 'alpha': 0.001, 'hidden_layer_sizes': (50, 50), 'learning_rate': 'constant', 'solver': 'sgd'},  # Best for L
    {'activation': 'tanh', 'alpha': 0.0001, 'hidden_layer_sizes': (100,), 'learning_rate': 'constant', 'solver': 'adam'}  # Best for XL
]
best_params_knn = [
    {'algorithm': 'brute', 'n_neighbors': 7, 'p': 1, 'weights': 'uniform'},  # Best for S
    {'algorithm': 'ball_tree', 'n_neighbors': 3, 'p': 1, 'weights': 'distance'},  # Best for L
    {'algorithm': 'brute', 'n_neighbors': 7, 'p': 2, 'weights': 'distance'}  # Best for XL
]

# Migliori iperparametri degli algoritmi (scelti sulla base dell'esito dei test in test_amazon_ml_analysis_best_score.py)
best_param_cart = best_params_cart[1]
best_param_random_forest = best_params_random_forest[2]
best_param_svc = best_params_svc[1]
best_param_gradient_boosting = best_params_gradient_boosting[2]
best_param_logistic_regression = best_params_logistic_regression[2]
best_param_mlp = best_params_mlp[0]
best_param_knn = best_params_knn[0]

# Classifiers
classifiers_map = {
    cart_alg_name: DecisionTreeClassifier(**best_param_cart),
    random_forest_alg_name: RandomForestClassifier(**best_param_random_forest),
    svm_alg_name: SVC(**best_param_svc),
    gradient_boosting_alg_name: GradientBoostingClassifier(**best_param_gradient_boosting),
    logistic_regression_alg_name: LogisticRegression(**best_param_logistic_regression),
    neural_network_alg_name: MLPClassifier(**best_param_mlp),
    k_nearest_neighbors_alg_name: KNeighborsClassifier(**best_param_knn)
}

# Opzionali: usati per test alternativi
optional_classifiers_map = {
    "CART ENTROPY": DecisionTreeClassifier(criterion="entropy", random_state=0),
    "EXTRA TREE": ExtraTreeClassifier(random_state=0),
    "RF GINI DEFAULT": RandomForestClassifier(random_state=0),
    "HIST GB": HistGradientBoostingClassifier(random_state=0),
    "SVC RBF DEFAULT": SVC(random_state=0),
    "GB DEFAULT": GradientBoostingClassifier(random_state=0),
    "SGD Classifier": SGDClassifier(random_state=0),
    "LR Default": LogisticRegression(random_state=0),
    "PERCEPTRONS DEFAULT": Perceptron(random_state=0),
    "KNN Default": KNeighborsClassifier()
}

# Algorithms List
algorithms = list(classifiers_map.keys())
optional_algorithms = list(optional_classifiers_map.keys())

# Dashboard Algorithm Input Option
algorithms_options = algorithms.copy()
algorithms_options.insert(0, all_algorithms)

# Lista di opzioni disponibili nella dashboard: utile ai test sulle varie combinazioni
min_sellers = [num for num in range(3, 11)]
nbb_sellers = [num for num in range(3, 11)]
test_sizes = [num/10 for num in range(1, 5)]
amazon_bb = [True, False]
amazon_nbb = [True, False]
new_bb = [True, False]
new_nbb = [True, False]

# Cross-validation options
hold_out_option = None
k_fold_option = KFold(n_splits=10)
stratified_k_fold_option = StratifiedKFold(n_splits=10, shuffle=True)
repeated_k_fold_option = RepeatedKFold(n_splits=10, n_repeats=3)
cross_validation_options = [hold_out_option, k_fold_option, stratified_k_fold_option, repeated_k_fold_option]
