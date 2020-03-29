import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
import numpy as np
import urllib.request
import urllib.error


# Funkcja parsująca atrybut trending_date do struktury Timestamp
def trending_date_to_timestamp(trending_date):
    date_parts = list(map(int, str(trending_date).split(sep='.')))
    return pd.Timestamp(2000 + date_parts[0], date_parts[2], date_parts[1])


# Funkcja obliczająca liczbę tagów z atrybutu tags
def tags_to_number_of_tags(tags):
    return 0 if tags == "[none]" else len(str(tags).split(sep='|'))


# Funkcja pomocnicza do wykresu liczba video z przypisaną kategorią vs liczba video bez przypisanej kategorii
def value_vs_non_value_in_category_id(category_id):
    return "No" if str(category_id) == "nan" else "Yes"


# Funkcja wydobywająca nazwę kategorii video wraz z ID
def extract_category_with_id_from_json_items(items):
    items_str = str(items)
    category_id = items_str[items_str.index("id\': \'") + 6:items_str.index("\', \'snippet")]
    category = items_str[items_str.index("title\': \'") + 9:items_str.index("\', \'assignable")]
    return int(category_id), category


# Funkcja pobierająca miniaturke z podanego linku
def download_thumbnail(thumbnail_link, video_id):
    try:
        resp = urllib.request.urlopen(thumbnail_link)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imwrite("thumbnails\\" + video_id + ".png", image)
    except urllib.error.HTTPError:
        pass


# Funkcja wyliczająca średnie RGB dla miniaturki filmu
def extract_average_rgb(video_id):
    try:
        image = cv2.imread("thumbnails\\" + video_id + ".png")
        avg_color_per_row = np.average(image, axis=0)
        return np.average(avg_color_per_row, axis=0)
    except:
        return "", "", ""


# Załadowanie danych z pliku
data_GB = pd.read_csv("GB_videos_5p.csv", delimiter=';', encoding='latin1')
data_US = pd.read_csv("US_videos_5p.csv", delimiter=';')

# Dodanie atrybutu country, który rozróżnia dane pochodzące z US i GB
data_GB['country'] = "GB"
data_US['country'] = "US"

# Złączenie danych w jeden zbiór
data = pd.concat([data_GB, data_US])
data = data.reset_index(drop=True)

# Zmiana nazwy atrybuty na poprawną (bez spacji na końcu)
data = data.rename(columns={"description ": "description"})

# Zmiana struktury danych atrybutu trending_date
data['trending_date'] = data['trending_date'].map(lambda trending_date: trending_date_to_timestamp(trending_date))

# Utworzenie mappingów na potrzeby kolejnych atrybutów
video_id_to_trending_count_mapping = data['video_id'].value_counts().to_dict()
video_id_to_first_trending_date_mapping = data.sort_values('trending_date').drop_duplicates("video_id") \
    .set_index('video_id').to_dict()['trending_date']

# Usunięcie duplikatów filmów po video_id
data = data.sort_values('views', ascending=False).drop_duplicates("video_id").sort_index().reset_index(drop=True)

# Utworzenie atrybutów: liczba wystąpień w zakładce Trending oraz data pierwszego pojawienia się filmu w zakładce Trending
data['trending_count'] = data['video_id'].map(lambda video_id: video_id_to_trending_count_mapping[video_id])
data['first_trending_date'] = data['video_id'].map(lambda video_id: video_id_to_first_trending_date_mapping[video_id])

# Zmiana nazwy atrybutu, który tak naprawdę jest teraz ostatnia datą wystąpienia filmiku w zakładce Trending
data = data.rename(columns={"trending_date": "last_trending_date"})

# Utworzenie nowych atrybutów na podstawie już obecnych
data['likes_views_ratio'] = data['likes'] / data['views']
data['dislikes_views_ratio'] = data['dislikes'] / data['views']
data['comment_count_views_ratio'] = data['comment_count'] / data['views']

# Dodanie atrybutów: długości tytułu oraz długości opisu
data['title_length'] = data.apply(lambda row: len(row['title']), axis=1)
data['description_length'] = data.apply(lambda row: len(str(row['description'])), axis=1)

# Uproszczenie danych atrybutu publish_time - usunięcie czasu, zostawienie tylko daty
data['publish_time'] = data['publish_time'].map(lambda publish_time: pd.Timestamp(pd.Timestamp(publish_time).date()))

# Utworzenie dwóch nowych atrybutów: rok oraz miesiąc publikacji
data['publish_time_year'] = data['publish_time'].map(lambda publish_time: publish_time.year)
data['publish_time_month'] = data['publish_time'].map(lambda publish_time: publish_time.month)

# Utworzenie atrybutu, który opisuje ile czasu (w dniach) video potrzebowało aby pojawić się w proponowanych
data['days_from_publish_time_to trending_date'] = data['first_trending_date'] - data['publish_time']
data['days_from_publish_time_to trending_date'] = data['days_from_publish_time_to trending_date'].map(
    lambda timedelta: timedelta.days)

# Dodanie atrybutów: liczby tagów w atrybucie tags oraz liczba linków w opisie
data['number_of_tags'] = data['tags'].map(lambda tags: tags_to_number_of_tags(tags))
data['number_of_links'] = data['description'].map(lambda description: str(description).count("http"))

for column in ['number_of_tags', 'number_of_links', 'title_length', 'description_length']:
    # Rysowanie wykresów pudełkowych interesujących atrybutów liczbowych (pierwszy wykres - całość danych, drugi wykres -
    # dane w podziale na kraj US lub GB)
    data.boxplot(column=[column])
    data.boxplot(by='country', column=[column])
    plt.suptitle('')
    plt.show()

    # Wypisanie statystyk zwizualizowanych na wcześniejszych wykresach pudełkowych
    print(data[column].describe())
    print(data.groupby('country')[column].describe())

# Załadowanie pliku z opisem kategorii (zawartość pliku GB zawiera się w zawartości pliku US jeśli chodzi o przypisanie nazwy kategorii do ID)
category_names = pd.read_json('US_category_id.json')

# Przemapowanie ID kategorii na jej nazwę
category_mapping = dict(
    category_names['items'].map(lambda items: extract_category_with_id_from_json_items(items)).tolist())
data['category_id'].replace(category_mapping, inplace=True)

# W związku z zastąpieniem ID kategorii przez jej nazwę to zmiana nazwy atrybutu
data = data.rename(columns={"category_id": "category"})

# Rysowanie wykresu obrazującego rozkład kategorii wśród video z przypisanymi kategoriami
category_count_plot = sns.countplot(x='category', data=data)
category_count_plot.set_xticklabels(category_count_plot.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()

# Rysowanie wykresu obrazującego porównanie liczby video z przypisaną kategorią do liczby video bez przypisanej kategorii
value_count = data['category'].map(lambda category_id: value_vs_non_value_in_category_id(category_id)).value_counts()
sns.barplot(value_count.index, value_count.values).set_title("Video has category")
plt.show()

# Wypisanie statystyk odnośnie liczby video z daną kategorią (lub bez)
print(data['category'].value_counts(dropna=False))

# Wykres liczby video w zależności od miesiąca w którym zostały opublikowane
sns.countplot(x='publish_time_month', data=data)
plt.show()

for group in ['publish_time_month', 'category']:
    for column in ['views', 'likes', 'comment_count']:
        # Rysowanie wykresów pudełkowych dla wybranych atrybutów
        # bez obserwacji odstających - aby wykres był czytelniejszy
        data.boxplot(by=group, column=[column], showfliers=False)
        if group == 'category':
            plt.xticks(rotation='vertical')
        plt.suptitle('')
        plt.show()

        # Wypisanie statystyk zwizualizowanych na wcześniejszych wykresach
        print(data.groupby(group)[column].describe())

# Wykres video z włączonymi komentarzami vs video z wyłączonymi komentarzami
sns.countplot(x='comments_disabled', data=data)
plt.show()

for column in ['views', 'likes']:
    # Rysowanie wykresów pudełkowych dla wybranych atrybutów
    # bez obserwacji odstających - aby wykres był czytelniejszy
    data.boxplot(by='comments_disabled', column=[column], showfliers=False)
    plt.suptitle('')
    plt.show()
    # Wypisanie statystyk zwizualizowanych na wcześniejszych wykresach
    print(data.groupby('comments_disabled')[column].describe())

# Wykres video z włączonymi ocenami vs video z wyłączonymi ocenami
sns.countplot(x='ratings_disabled', data=data)
plt.show()

for column in ['views', 'comment_count']:
    # Rysowanie wykresów pudełkowych dla wybranych atrybutów
    # bez obserwacji odstających - aby wykres był czytelniejszy
    data.boxplot(by='ratings_disabled', column=[column], showfliers=False)
    plt.suptitle('')
    plt.show()
    # Wypisanie statystyk zwizualizowanych na wcześniejszych wykresach
    print(data.groupby('ratings_disabled')[column].describe())

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

# Część kodu odpowiedzialna za pobranie miniaturek
# for _, row in data.iterrows():
#     download_thumbnail(row['thumbnail_link'], row['video_id'])

# Utworzenie trzech nowych atrybutów opartych na średnich wartościach dla każdego z kanałów RGB
data['average_red'], data['average_green'], data['average_blue'] = \
    zip(*data['video_id'].map(lambda video_id: extract_average_rgb(video_id)))
