from unittest import TestCase

from parameterized import parameterized

from data_analysis.scripts.amazon_ML_analysis import exec_ml_analysis_by_clf
from data_analysis.scripts.amazon_ML_constants import S_inputs, \
    L_inputs, XL_inputs, feature_columns_opt, classifiers_map, hold_out_option, repeated_k_fold_option, \
    stratified_k_fold_option, k_fold_option
from data_analysis.scripts.amazon_data_normalizer import normalize_amazon_data
from data_analysis.scripts.amazon_data_reader import import_input_json_files_from_dir


def generate_test_input_1():
    test_inputs = []
    for algorithm in classifiers_map.keys():
        for test_size in [None, 0.1, 0.2, 0.3, 0.4]:
            for input_size in [S_inputs, L_inputs, XL_inputs]:
                test_inputs.append([algorithm, classifiers_map[algorithm], test_size, input_size])
    return test_inputs


def generate_test_input_2():
    test_inputs = []
    for cv_option in [k_fold_option, stratified_k_fold_option, repeated_k_fold_option]:
        for algorithm in classifiers_map.keys():
            for input_size in [S_inputs, L_inputs, XL_inputs]:
                test_inputs.append([algorithm, classifiers_map[algorithm], input_size, cv_option])
    return test_inputs


# def generate_test_input_simple():
#     test_inputs = []
#     for cv_option in [repeated_k_fold_option]:
#         for algorithm in classifiers_map.keys():
#             for input_size in [S_inputs]:
#                 test_inputs.append([algorithm, classifiers_map[algorithm], input_size, cv_option])
#             break
#     return test_inputs


# Da lanciare con workspace la cartella scripts
class Test(TestCase):

    @parameterized.expand(generate_test_input_1())
    def test_accuracy_analysis_with_hold_out(self, algorithm, clf, test_size, dir_path_test_files):
        amazon_data = import_input_json_files_from_dir(dir_path_test_files)
        normalized_data = normalize_amazon_data(amazon_data)
        print("Dataset size:", len(normalized_data))

        perm_importance, accuracy = exec_ml_analysis_by_clf(clf, algorithm, normalized_data, test_size, feature_columns_opt, hold_out_option)
        print(f"Accuracy score: {accuracy}")
        self.assertTrue(round(accuracy, 2) >= 0.95)

    @parameterized.expand(generate_test_input_2())
    def test_accuracy_analysis_with_cross_validation(self, algorithm, clf, dir_path_test_files, cv_option):
        amazon_data = import_input_json_files_from_dir(dir_path_test_files)
        normalized_data = normalize_amazon_data(amazon_data)
        print("Dataset size:", len(normalized_data))

        perm_importance, accuracy = exec_ml_analysis_by_clf(clf, algorithm, normalized_data, None, feature_columns_opt, cv_option)
        print(f"Accuracy score: {accuracy}")
        self.assertTrue(round(accuracy, 2) >= 0.95)

    # @parameterized.expand(generate_test_input_simple())
    # def test_accuracy_analysis_with_cross_validation(self, algorithm, clf, dir_path_test_files, cv_option):
    #     amazon_data = import_input_json_files_from_dir(dir_path_test_files)
    #     normalized_data = normalize_amazon_data(amazon_data)
    #     print("Dataset size:", len(normalized_data))
    #
    #     perm_importance, accuracy = exec_ml_analysis_by_clf(clf, algorithm, normalized_data, None,
    #                                                         feature_columns_opt, cv_option)
    #     print(f"Accuracy score: {accuracy}")
    #     self.assertTrue(round(accuracy, 2) >= 0.95)

