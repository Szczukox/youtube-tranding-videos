import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math


def trending_date_to_timestamp(trending_date):
    date_parts = list(map(int, str(trending_date).split(sep='.')))
    return pd.Timestamp(2000 + date_parts[0], date_parts[2], date_parts[1])


def tags_to_number_of_tags(tags):
    return 0 if tags == "[none]" else len(str(tags).split(sep='|'))


def value_vs_non_value_in_category_id(category_id):
    return "No" if math.isnan(category_id) else "Yes"


data_GB = pd.read_csv("GB_videos_5p.csv", delimiter=';', encoding='latin1')
data_US = pd.read_csv("US_videos_5p.csv", delimiter=';')

data_GB['country'] = "GB"
data_US['country'] = "US"

data = pd.concat([data_GB, data_US])

data = data.rename(columns={"description ": "description"})

data['title_length'] = data.apply(lambda row: len(row['title']), axis=1)
data['description_length'] = data.apply(lambda row: len(str(row['description'])), axis=1)

data['trending_date'] = data['trending_date'].map(lambda trending_date: trending_date_to_timestamp(trending_date))

data['publish_time'] = data['publish_time'].map(lambda publish_time: pd.Timestamp(pd.Timestamp(publish_time).date()))
data['publish_time_year'] = data['publish_time'].map(lambda publish_time: publish_time.year)
data['publish_time_month'] = data['publish_time'].map(lambda publish_time: publish_time.month)

data['days_from_publish_time_to trending_date'] = data['trending_date'] - data['publish_time']
data['days_from_publish_time_to trending_date'] = data['days_from_publish_time_to trending_date'].map(
    lambda timedelta: timedelta.days)

data['number_of_tags'] = data['tags'].map(lambda tags: tags_to_number_of_tags(tags))

data['number_of_links'] = data['description'].map(lambda description: str(description).count("http"))

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

print(data['number_of_tags'].describe())
print(data['number_of_links'].describe())
print(data['title_length'].describe())
print(data['description_length'].describe())
print(data.groupby('country')['number_of_tags'].describe())
print(data.groupby('country')['number_of_links'].describe())
print(data.groupby('country')['title_length'].describe())
print(data.groupby('country')['description_length'].describe())

sns.countplot(x='category_id', data=data)
plt.show()

value_count = data['category_id'].map(lambda category_id: value_vs_non_value_in_category_id(category_id)).value_counts()
sns.barplot(value_count.index, value_count.values).set_title("Video has category ID")
plt.show()

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
print(data['category_id'].value_counts(dropna=False))
print(data.corr())
