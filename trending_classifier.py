import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

# Załadowanie danych
trending = pd.read_csv("trending.csv", sep=";")
non_trending = pd.read_csv("non_trending.csv", sep=";")

# Dodanie klasy do danych
trending["is_trending"] = True
non_trending["is_trending"] = False

# Połączenie zbioru danych w jeden
data = pd.concat([trending, non_trending], sort=False)
data = data.reset_index(drop=True)

# Z całego zbioru danych wybieramy te filmy, które mają miniaturkę
data = data.loc[data["average_red"].notna()]
data = data.loc[data["likes_views_ratio"].notna()]

# Wyznaczony zbiór dzielimy na zbiór atrybutów i klas
features = data[data.columns.difference(
    ["category", "video_id", "first_trending_date", "title", "channel_title", "publish_time", "tags", "thumbnail_link",
     "description", "country", "last_trending_date", "is_trending", "video_error_or_removed", "trending_count",
     "days_from_publish_time_to trending_date"], sort=False)].copy()
target = data["is_trending"].copy()

# Tworzymy i trenujemy klasyfikator
random_forest = RandomForestClassifier(max_depth=10, min_samples_leaf=4, min_samples_split=10, n_estimators=100,
                                       max_features='auto', random_state=12)
x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=12)
random_forest.fit(x_train, y_train)
y_pred = random_forest.predict(x_test)

# Statystyki klasyfikatora
print("Classification Report")
print(classification_report(y_test, y_pred))
print("Confusion Matrix")
print(confusion_matrix(y_test, y_pred))

mlp = MLPClassifier(alpha=1, max_iter=1000, random_state=12)
mlp.fit(x_train, y_train)
y_pred = mlp.predict(x_test)

# Statystyki klasyfikatora
print("Classification Report")
print(classification_report(y_test, y_pred))
print("Confusion Matrix")
print(confusion_matrix(y_test, y_pred))
