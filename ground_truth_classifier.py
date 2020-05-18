import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

# Załadowanie danych
data = pd.read_csv("trending.csv", sep=";")

# Z całego zbioru danych wybieramy te filmy, które mają opisaną kategorią i mają miniaturkę
data_with_category = data.loc[data["category"].notnull() & data["average_red"].notna()]

# Wyznaczony zbiór dzielimy na zbiór atrybutów i klas
features = data_with_category[data_with_category.columns.difference(
    ["category", "video_id", "first_trending_date", "title", "channel_title", "publish_time", "tags", "thumbnail_link",
     "description", "country", "last_trending_date"], sort=False)].copy()
target = data_with_category["category"].copy()

# Wyznaczamy wagi klas dla random forest
category_dict = data_with_category['category'].value_counts(dropna=True).to_dict()
max_category_count = max(category_dict.values())
category_weight = {k: max_category_count / v for k, v in category_dict.items()}

# Tworzymy i trenujemy klasyfikator
random_forest = RandomForestClassifier(max_depth=10, min_samples_leaf=4, min_samples_split=10, n_estimators=300,
                                       max_features='auto', class_weight=category_weight, random_state=12)
x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.1, random_state=12)
random_forest.fit(x_train, y_train)
y_pred = random_forest.predict(x_test)

# Statystyki klasyfikatora
print("Classification Report")
print(classification_report(y_test, y_pred))
print("Confusion Matrix")
print(confusion_matrix(y_test, y_pred))

# Ground truth
ground_truth = pd.read_csv("trending_with_category.csv", sep=";")
ground_truth = ground_truth.loc[ground_truth["category"].notnull() & ground_truth["average_red"].notna()]

features_ground_truth = ground_truth[ground_truth.columns.difference(
    ["category", "video_id", "first_trending_date", "title", "channel_title", "publish_time", "tags", "thumbnail_link",
     "description", "country", "last_trending_date"], sort=False)].copy()
target_ground_truth = ground_truth["category"].copy()

# train_ground_truth, test_ground_truth, a, b = train_test_split(features, target, test_size=0, random_state=12)

pred_ground_truth = random_forest.predict(features_ground_truth)

# Statystyki klasyfikatora
print("Classification Report")
print(classification_report(target_ground_truth, pred_ground_truth))
print("Confusion Matrix")
print(confusion_matrix(target_ground_truth, pred_ground_truth))
