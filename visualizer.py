import matplotlib.pyplot as plt
from pandas import DataFrame
from scipy.stats import norm, probplot
import seaborn as sns
import pandas as pd
from my_types import dtypes
from sklearn.preprocessing import StandardScaler
import numpy as np
from wordcloud import WordCloud
from nltk.corpus import stopwords


class Visualizer:
  def __init__(self) -> None:
    pass

  def histo(self, df: DataFrame, param: str = 'price') -> None:
    # histogram
    sns.set(rc={'figure.figsize': (11.7, 8.27)})

    # histogram and normal probability plot
    sns.distplot(df[param], fit=norm)
    (mu, sigma) = norm.fit(df[param])
    print('\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu, sigma))
    fig = plt.figure()
    plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)], loc='best')
    plt.ylabel('Frequency')
    plt.title(f'{param} distribution')
    res = probplot(df[param], plot=plt)
    plt.show()

  # Kaisar
  def word_cloud(self, df: DataFrame) -> None:
    filtered_df = df[df['text'].notnull()]
    text1 = " ".join(title for title in filtered_df.text)
    russian_stopwords = stopwords.words("russian")
    word_cloud1 = WordCloud(collocations=False, background_color='white',
                            width=2048, height=1080, stopwords=russian_stopwords).generate(text1)

    # saving the image
    word_cloud1.to_file('word_cloud.png')

  def biv(self, df: DataFrame) -> None:
    # bivariate analysis saleprice/grlivarea
    var = 'general_area'
    data = pd.concat([df['price'], df[var]], axis=1)
    data.plot.scatter(x=var, y='price')

    # bivariate analysis saleprice/grlivarea
    var = 'TotalBsmtSF'
    data = pd.concat([df['price'], df[var]], axis=1)
    data.plot.scatter(x=var, y='price', ylim=(0, 800000))

  def std(self, df: DataFrame) -> None:
    # standardizing data
    price_scaled = StandardScaler().fit_transform(df['price'][:, np.newaxis])
    low_range = price_scaled[price_scaled[:, 0].argsort()][:10]
    high_range = price_scaled[price_scaled[:, 0].argsort()][-10:]
    print('outer range (low) of the distribution:')
    print(low_range)
    print('\nouter range (high) of the distribution:')
    print(high_range)

  def corr(self, df: DataFrame) -> None:
    # correlation matrix
    corrmat = df.corr()
    f, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(corrmat, vmax=.8, square=True)
    plt.show()

  def scatter(self, df: DataFrame, from_param: str, to_param: str = 'price') -> None:
    print(f'Scattering {from_param} to {to_param}')
    match dtypes[from_param]:
      case 'str':
        from_series = df[from_param].fillna('NaN')
        to_series = df[to_param].fillna('NaN')
      case _:
        from_series = df[from_param]  # .fillna('NaN')
        to_series = df[to_param]  # .fillna('NaN')

    fig, ax = plt.subplots()
    ax.scatter(x=from_series, y=to_series)
    plt.ylabel(to_param, fontsize=13)
    plt.xlabel(from_param, fontsize=13)
    plt.show()

  def scatters(self, df: DataFrame, from_params: list[str] = ['price', 'build_year', 'general_area']) -> None:
    # scatterplot
    sns.set()
    sns.pairplot(df[from_params], size=2.5)
    plt.show()

  def describe_column(self, df: DataFrame, column_name: str) -> None:
    print(f"Price column:\n{df[column_name].describe().apply(lambda x: format(x, 'f'))}\n")

    self.histo(df, column_name)

  def plot_missing_data(self, missing_data: DataFrame) -> None:
    f, ax = plt.subplots(figsize=(15, 12))
    plt.xticks(rotation=90)
    sns.barplot(x=missing_data[:20].index, y=missing_data['Percent'][:20] * 100)
    plt.xlabel('Features', fontsize=15)
    plt.ylabel('Percent of missing values', fontsize=15)
    plt.title('Percent missing data by feature', fontsize=15)
