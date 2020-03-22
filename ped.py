import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math


# Funkcja parsująca atrybut trending_date do struktury Timestamp
def trending_date_to_timestamp(trending_date):
    date_parts = list(map(int, str(trending_date).split(sep='.')))
    return pd.Timestamp(2000 + date_parts[0], date_parts[2], date_parts[1])


# Funkcja obliczająca liczbę tagów z atrybutu tags
def tags_to_number_of_tags(tags):
    return 0 if tags == "[none]" else len(str(tags).split(sep='|'))


# Funkcja pomocnicza do wykresu liczba video z przypisaną kategorią vs liczba video bez przypisanej kategorii
def value_vs_non_value_in_category_id(category_id):
    return "No" if math.isnan(category_id) else "Yes"


# Załadowanie danych z pliku
data_GB = pd.read_csv("GB_videos_5p.csv", delimiter=';', encoding='latin1')
data_US = pd.read_csv("US_videos_5p.csv", delimiter=';')

# Dodanie atrybutu country, który rozróżnia dane pochodzące z US i GB
data_GB['country'] = "GB"
data_US['country'] = "US"

# Złączenie danych w jeden zbiór
data = pd.concat([data_GB, data_US])

# Zmiana nazwy atrybuty na poprawną (bez spacji na końcu)
data = data.rename(columns={"description ": "description"})

# Dodanie atrybutów: długości tytułu oraz długości opisu
data['title_length'] = data.apply(lambda row: len(row['title']), axis=1)
data['description_length'] = data.apply(lambda row: len(str(row['description'])), axis=1)

# Zmiana struktury danych atrybutu trending_date
data['trending_date'] = data['trending_date'].map(lambda trending_date: trending_date_to_timestamp(trending_date))

# Uproszczenie danych atrybutu publish_time - usunięcie czasu, zostawienie tylko daty
data['publish_time'] = data['publish_time'].map(lambda publish_time: pd.Timestamp(pd.Timestamp(publish_time).date()))

# Utworzenie dwóch nowych atrybutów: rok oraz miesiąc publikacji
data['publish_time_year'] = data['publish_time'].map(lambda publish_time: publish_time.year)
data['publish_time_month'] = data['publish_time'].map(lambda publish_time: publish_time.month)

# Utworzenie atrybutu, który opisuje ile czasu (w dniach) video potrzebowało aby pojawić się w proponowanych
data['days_from_publish_time_to trending_date'] = data['trending_date'] - data['publish_time']
data['days_from_publish_time_to trending_date'] = data['days_from_publish_time_to trending_date'].map(
    lambda timedelta: timedelta.days)

# Dodanie atrybutów: liczby tagów w atrybucie tags oraz liczba linków w opisie
data['number_of_tags'] = data['tags'].map(lambda tags: tags_to_number_of_tags(tags))
data['number_of_links'] = data['description'].map(lambda description: str(description).count("http"))

# Rysowanie wykresów pudełkowych interesujących atrybutów liczbowych (pierwszy wykres - całość danych, drugi wykres -
# dane w podziale na kraj US lub GB)
data.boxplot(column=['number_of_tags'])
data.boxplot(by='country', column=['number_of_tags'])
plt.suptitle('')
plt.show()

data.boxplot(column=['number_of_links'])
data.boxplot(by='country', column=['number_of_links'])
plt.suptitle('')
plt.show()

data.boxplot(column=['title_length'])
data.boxplot(by='country', column=['title_length'])
plt.suptitle('')
plt.show()

data.boxplot(column=['description_length'])
data.boxplot(by='country', column=['description_length'])
plt.suptitle('')
plt.show()

# Wypisanie statystyk zwizualizowanych na wcześniejszych wykresach pudełkowych
print(data['number_of_tags'].describe())
print(data['number_of_links'].describe())
print(data['title_length'].describe())
print(data['description_length'].describe())
print(data.groupby('country')['number_of_tags'].describe())
print(data.groupby('country')['number_of_links'].describe())
print(data.groupby('country')['title_length'].describe())
print(data.groupby('country')['description_length'].describe())

# Rysowanie wykresu obrazującego rozkład kategorii wśród video z przypisanymi kategoriami
sns.countplot(x='category_id', data=data)
plt.show()

# Rysowanie wykresu obrazującego porównanie liczby video z przypisaną kategorią do liczby video bez przypisanej kategorii
value_count = data['category_id'].map(lambda category_id: value_vs_non_value_in_category_id(category_id)).value_counts()
sns.barplot(value_count.index, value_count.values).set_title("Video has category ID")
plt.show()

# Wypisanie statystyk odnośnie liczby video z daną kategorią (lub bez)
print(data['category_id'].value_counts(dropna=False))

# Rysowanie wykresu korelacji atrybutów
correlation_matrix = data.corr()
ax = sns.heatmap(correlation_matrix,
                 vmin=-1, vmax=1, center=0,
                 cmap=sns.diverging_palette(20, 220, n=200),
                 square=True)
sns.set(font_scale=0.01)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)
plt.show()

# Wypisanie macierzy korelacji
print(data.corr())
