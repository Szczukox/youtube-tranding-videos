import os.path
import urllib.error
import urllib.request

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Funkcja mapująca thumbnail_link na video_id
def map_video_id_from_thumbnail_link(thumbnail_link):
    return thumbnail_link.split(sep='/')[-2]


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


# Funkcja pobierająca miniaturke w rozdzielczości 120x90 z podanego linku
def download_thumbnail(thumbnail_link, video_id):
    if not os.path.exists("thumbnails\\" + video_id + ".png"):
        try:
            resp = urllib.request.urlopen(thumbnail_link)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cv2.imwrite("thumbnails\\" + video_id + ".png", image)
        except urllib.error.HTTPError:
            pass


# Funkcja pobierająca miniaturke w rozdzielczości 480x360 z podanego linku
def download_hq_thumbnail(thumbnail_link, video_id):
    if not os.path.exists("thumbnails_hq\\" + video_id + ".png"):
        try:
            index = thumbnail_link.find("default.jpg")
            resp = urllib.request.urlopen(thumbnail_link[:index] + "hq" + thumbnail_link[index:])
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cv2.imwrite("thumbnails_hq\\" + video_id + ".png", image)
        except urllib.error.HTTPError:
            pass


# Funkcja wczytująca i przetwarzająca miniaturkę (obicięcie 10 górnych i dolnych pikseli w celi wyeliminowania czarnych pasków)
def load_and_process_rgb_thumbnail(video_id):
    try:
        image = cv2.imread("thumbnails\\" + video_id + ".png")[10:-10]
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return np.concatenate((extract_average(image), extract_mode(image),
                               extract_average(image_hsv), extract_mode(image_hsv),
                               extract_count_pixels_by_hue(image_hsv), extract_rms_contrast(image_gray)), axis=None)
    except:
        return 19 * ([float("NaN")])


# Funkcja wyliczająca średnie dla miniaturki filmu
def extract_average(image):
    return image.mean(axis=0).mean(axis=0)


# Funkcja wyliczająca dominantę dla miniaturki filmu
def extract_mode(image):
    colors, count = np.unique(image.reshape(-1, image.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]


# Funkcja zliczająca pixele w ramach poszczególnych przedziałów wartości hue
def extract_count_pixels_by_hue(image_hsv):
    hue = image_hsv[:, :, 0]
    red = np.size(hue[(hue < 15) | (hue >= 165)])
    yellow = np.size(hue[(hue >= 15) & (hue < 45)])
    green = np.size(hue[(hue >= 45) & (hue < 75)])
    cyan = np.size(hue[(hue >= 75) & (hue < 105)])
    blue = np.size(hue[(hue >= 105) & (hue < 135)])
    magenta = np.size(hue[(hue >= 135) & (hue < 165)])
    return red, yellow, green, cyan, blue, magenta


# Funckja wyliczająca kontrast RMS (root mean square)
def extract_rms_contrast(image_gray):
    return image_gray.std()


def assign_category_from_youtube_api(video_id, category):
    if str(category) == "nan":
        values = trending_with_category.loc[trending_with_category["video_id"] == video_id]["category"].values
        if values.size != 0:
            return values[0]
    return category


# Załadowanie danych z pliku
data_GB = pd.read_csv("GB_videos_5p.csv", delimiter=';', encoding='latin1')
data_US = pd.read_csv("US_videos_5p.csv", delimiter=';')

# Dodanie atrybutu country, który rozróżnia dane pochodzące z US i GB
data_GB['country'] = "GB"
data_US['country'] = "US"

# Złączenie danych w jeden zbiór
data = pd.concat([data_GB, data_US])
data = data.reset_index(drop=True)

# Przypisanie nowych video_id dla wpisów z 'video_id' == #NAZWA? na podstawie thumbnail_link
data.loc[data['video_id'] == "#NAZWA?", "video_id"] = \
    data['thumbnail_link'].map(lambda thumbnail_link: map_video_id_from_thumbnail_link(thumbnail_link))

# Zmiana nazwy atrybuty na poprawną (bez spacji na końcu)
data = data.rename(columns={"description ": "description"})

# Zmiana struktury danych atrybutu trending_date
data['trending_date'] = data['trending_date'].map(lambda trending_date: trending_date_to_timestamp(trending_date))

# Utworzenie mappingów na potrzeby kolejnych atrybutów
video_id_to_trending_count_mapping = data['video_id'].value_counts().to_dict()
video_id_to_last_trending_date_mapping = data.sort_values('trending_date', ascending=False).drop_duplicates("video_id") \
    .set_index('video_id').to_dict()['trending_date']

# Usunięcie duplikatów filmów po video_id
data = data.sort_values('views').drop_duplicates("video_id").sort_index().reset_index(drop=True)

# Część kodu odpowiedzialna za pobranie miniaturek
# for _, row in data.iterrows():
#     download_hq_thumbnail(row['thumbnail_link'], row['video_id'])

# Utworzenie atrybutów: liczba wystąpień w zakładce Trending oraz data ostatniego pojawienia się filmu w zakładce Trending
data['trending_count'] = data['video_id'].map(lambda video_id: video_id_to_trending_count_mapping[video_id])
data['last_trending_date'] = data['video_id'].map(lambda video_id: video_id_to_last_trending_date_mapping[video_id])

# Zmiana nazwy atrybutu, który tak naprawdę jest teraz pierwszą datą wystąpienia filmiku w zakładce Trending
data = data.rename(columns={"trending_date": "first_trending_date"})

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

# Przypisanie kategorii z Youtube API dla tych filmów, które miały pustą kategorię
trending_with_category = pd.read_csv("trending_with_category.csv", sep=";")
data["category"] = data\
    .apply(lambda row: assign_category_from_youtube_api(row["video_id"], row["category"]), axis=1)

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

# Utworzenie atrvbutów wizualnych
data['average_red'], data['average_green'], data['average_blue'], \
data['mode_red]'], data['mode_green'], data['mode_blue'], \
data['average_hue'], data['average_saturation'], data['average_value'], \
data['mode_hue'], data['mode_saturation'], data['mode_value'], \
data['hue_red'], data['hue_yellow'], data['hue_green'], data['hue_cyan'], data['hue_blue'], data['hue_magenta'], \
data['rms_contrast'] = zip(*data['video_id'].map(lambda video_id: load_and_process_rgb_thumbnail(video_id)))

# Dodanie atrybutów wyrażających emocję na miniaturce ('angry','disgust','fear','happy','sad','surprise','neutral')
emotion_vectors = pd.read_csv("emotions_hq.csv", delimiter=',')
data = pd.merge(data, emotion_vectors, how='left', on='video_id')

# Wykres pudełkowy liczby pikseli obrazka dla każdego z odcieni hue
hue_colors = ['hue_red', 'hue_yellow', 'hue_green', 'hue_cyan', 'hue_blue', 'hue_magenta']
data.boxplot(column=hue_colors)
plt.title("Liczba pikseli w danym odcieniu Hue")
plt.show()

# Wypisanie statystyk
for column in hue_colors:
    print(data[column].describe())

# Wypisanie statystyk liczby emocji dla wszystkich obrazków w podziale na typ
emotion_count = {}
for emotion in ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']:
    count = np.count_nonzero(data[emotion] > 0)
    emotion_count[emotion] = count
    print(emotion + ": " + str(count))

# Rysowanie wykresu liczby emocji dla wszystkich obrazków w podziale na typ
plt.bar(emotion_count.keys(), emotion_count.values())
plt.title("Emotion counts")
plt.show()

# Rysowanie wykresu korelacji atrybutów
f = plt.figure(figsize=(30, 30))
plt.matshow(data.corr(), fignum=f.number, cmap=plt.cm.get_cmap("coolwarm"))
plt.xticks(range(data.corr().shape[1]), data.corr().columns, fontsize=20, rotation=90)
plt.yticks(range(data.corr().shape[1]), data.corr().columns, fontsize=20)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=15)
plt.suptitle("Correlation", fontsize=64)
plt.show()

# Wypisanie macierzy korelacji
print(data.corr())
