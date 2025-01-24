import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import train_test_split

from logger import logging


def train_and_predict(df, clf, name, test_size, feature_columns, target_columns):
    encoded_features = df[feature_columns]
    encoded_target = df[target_columns]

    x_train, x_test, y_train, y_test = train_test_split(encoded_features, encoded_target,
                                                        test_size=test_size if test_size is not None and test_size > 0 else None, random_state=0)
    clf = clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)

    logging.info("Confusion Matrix:\n" + str(confusion_matrix(y_test, y_pred)))
    logging.info('Classification Report:\n' + str(classification_report(y_true=y_test, y_pred=y_pred)))
    accuracy = accuracy_score(y_test, y_pred)
    logging.info("Accuracy Score:" + str(accuracy))

    logging.info('Features Importance List:')
    perm_importance = pd.Series((permutation_importance(clf, x_test, y_test, random_state=42)).importances_mean,
                                index=feature_columns)
    if min(perm_importance) < 0:
        perm_importance = perm_importance + abs(min(perm_importance))
    perm_importance = perm_importance / sum(perm_importance)
    importance = pd.DataFrame(perm_importance).T
    importance.insert(0, "model", name)
    perm_importance = perm_importance.sort_values(ascending=False)
    logging.info(perm_importance)
    return perm_importance, accuracy

