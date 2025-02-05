from sklearn.tree import DecisionTreeClassifier

from amazon_ML_constants import classifiers_map, optional_classifiers_map, target_features, \
    algorithms, cross_validation_options
from amazon_ML_functions import train_and_predict
from logger import logging


def get_classifier_by_name(name):
    if name in classifiers_map.keys():
        classifier = classifiers_map.get(name)
    elif name in optional_classifiers_map.keys():
        classifier = optional_classifiers_map.get(name)
    else:
        classifier = DecisionTreeClassifier()
        logging.info("Classifier not found! DecisionTreeClassifier applied!")
    return classifier


def exec_ml_analysis_by_clf(clf, name, data, radio_cv_option, test_size, feature_columns):
    perm_importance, accuracy = train_and_predict(data, clf, name, test_size, feature_columns, target_features,
                                                  cross_validation_options[radio_cv_option])

    return perm_importance, accuracy


def exec_ml_analysis(name, data, radio_cv_option, test_size, feature_columns):
    # Create the classifier by name
    clf = get_classifier_by_name(name)

    return exec_ml_analysis_by_clf(clf, name, data, radio_cv_option, test_size, feature_columns)


def exec_all_ml_analysis(data, radio_cv_option, test_size, feature_columns, set_progress):
    ml_analysis_output = []
    alg_count = len(algorithms)
    alg_index = 0
    set_progress((str(alg_index), str(alg_count)))
    for alg_name in algorithms:
        perm_importance, accuracy = exec_ml_analysis(alg_name, data, radio_cv_option, test_size, feature_columns)
        ml_analysis_output.append({"alg_name": alg_name, "perm_importance": perm_importance, "accuracy": accuracy})
        set_progress((str(alg_index + 1), str(alg_count)))
        alg_index += 1
    return ml_analysis_output

