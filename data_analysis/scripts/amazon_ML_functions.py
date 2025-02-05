import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold

from logger import logging


def train_and_predict(df, clf, name, test_size, feature_columns, target_columns, cv=None):
    if cv is not None:
        print("Cross Validation to apply: ", str(cv))
        return train_and_predict_with_cross_validation(df, clf, name, feature_columns, target_columns, cv)

    encoded_features = df[feature_columns]
    encoded_target = df[target_columns]

    x_train, x_test, y_train, y_test = train_test_split(encoded_features, encoded_target,
                                                        test_size=test_size if test_size is not None and test_size > 0 else None)
    clf = clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)

    logging.info("Confusion Matrix:\n" + str(confusion_matrix(y_test, y_pred)))
    logging.info('Classification Report:\n' + str(classification_report(y_true=y_test, y_pred=y_pred)))
    accuracy = accuracy_score(y_test, y_pred)
    logging.info("Accuracy Score:" + str(accuracy))

    logging.info('Features Importance List:')
    perm_importance = pd.Series((permutation_importance(clf, x_test, y_test, random_state=42, n_jobs=-1)).importances_mean,
                                index=feature_columns)
    if min(perm_importance) < 0:
        perm_importance = perm_importance + abs(min(perm_importance))
    perm_importance = perm_importance / sum(perm_importance)
    perm_importance = perm_importance.sort_values(ascending=False)
    logging.info(perm_importance)
    return perm_importance, accuracy


def train_and_predict_with_cross_validation(df, clf, name, feature_columns, target_columns, cv):
    encoded_features = df[feature_columns]
    encoded_target = df[target_columns]

    accuracy_scores = []
    feature_importances = pd.DataFrame(columns=['model', 'fold'])

    fold_index = 0
    for train_index, test_index in cv.split(encoded_features, encoded_target):
        x_train, x_test = encoded_features.iloc[train_index], encoded_features.iloc[test_index]
        y_train, y_test = encoded_target.iloc[train_index], encoded_target.iloc[test_index]

        clf = clf.fit(x_train, y_train)

        y_pred = clf.predict(x_test)

        # Calculate accuracy for each fold
        accuracy = accuracy_score(y_test, y_pred)
        accuracy_scores.append(accuracy)

        # Extract feature importances for each fold
        perm_importance = pd.Series((permutation_importance(clf, x_test, y_test, random_state=42, n_jobs=-1)).importances_mean,
                                    index=feature_columns)
        if min(perm_importance) < 0:
            perm_importance = perm_importance + abs(min(perm_importance))
        perm_importance = perm_importance / sum(perm_importance)
        importance = pd.DataFrame(perm_importance).T
        importance.insert(0, "model", name)
        importance.insert(1, "fold", fold_index + 1)  # Add fold number
        feature_importances = pd.concat([feature_importances, importance], ignore_index=True)
        fold_index += 1

    logging.info("Average Accuracy Score Across Folds: " + str(np.mean(accuracy_scores)))
    logging.info("Min Accuracy Score Across Folds: " + str(np.min(accuracy_scores)))
    logging.info("Max Accuracy Score Across Folds: " + str(np.max(accuracy_scores)))

    logging.info('Features Importance Avg List:')
    # Average feature importance across folds
    feature_importances_avg = feature_importances.groupby(['model'])[feature_columns].mean()
    feature_importances_avg = feature_importances_avg.reset_index()
    feature_importances_avg = feature_importances_avg[feature_columns].T.sort_values(by=0, ascending=False)
    logging.info(feature_importances_avg)

    return feature_importances_avg, np.mean(accuracy_scores)

