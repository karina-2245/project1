import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#импортируем три дата сета с информацией о фильмах, их рейтинге, и пользователях стриминг-сервиса
movies_data = pd.read_csv('/Users/grigorovakarina/Downloads/archive/Netflix_Dataset_Movie.csv')
ratings = pd.read_csv('/Users/grigorovakarina/Downloads/archive/Netflix_Dataset_Rating.csv')
users = pd.read_csv('/Users/grigorovakarina/Downloads/netflix_users.csv')

#проверим все три дата сета на наличие пустых значений
#print(movies_data.isnull())
#print(movies_data.isnull().sum())

#print(ratings.isnull())
#print(ratings.isnull().sum())

#print(users.isnull())
#print(users.isnull().sum())

#заполним пустые значения
ratings['Rating'] = ratings['Rating'].fillna(ratings['Rating'].mean())
users['Age'] = users['Age'].fillna(users['Age'].median())

#объединим таблицы movie_data и movies_ratings:
merged_df = pd.merge(movies_data, ratings, on = 'Movie_ID')
rating_user = pd.merge(users, merged_df, on = 'User_ID')
print(rating_user.head())

#Аналитические запросы
#1. Самый популярный жанр
rating_user = rating_user.assign(Genres=rating_user['Favorite_Genre'].str.split('|')).explode('Favorite_Genre')
most_popular_genre = rating_user['Favorite_Genre'].value_counts().idxmax()
print(f'Самый популярный жанр среди пользователей:\n{most_popular_genre}')

#1.2 Самый популярный жанр для возрастных групп
rating_user['Age_Group'] = pd.cut(rating_user['Age'],
                                  bins = [18,30,45,60,90],
                                  labels= ['18-30', '30-45', '45-60', '60-90'])
print(rating_user.head())
pivot = pd.pivot_table(rating_user,
                    index = 'Favorite_Genre',
                    columns = 'Age_Group',
                    aggfunc = 'mean',
                    values = 'Rating')
print(f'Сводная таблица:\n {pivot.round(2)}')
popular_genre = pivot.idxmax(axis=0)
popular_genre_df = popular_genre.reset_index()
popular_genre_df.columns = ['Age_Group', 'Most_Popular_Genre']
print(f'Самый популярный жанр для каждой возрастной группы:\n{popular_genre_df}')

#2. Средний рейтинг фильмов за каждое десятилетие
bins1=[1960, 1970, 1980, 1990, 2000]
rating_user['Decade'] = pd.cut(
    rating_user['Year'],
    bins=bins1,
    right=False,
    labels=[f'{bins1[i]}' for i in range(len(bins1) - 1)])

avg_rating_by_year = round(rating_user.groupby('Decade')['Rating'].mean(),2)
print(f'Средний рейтинг фильмов за каждое десятилетие:\n{avg_rating_by_year}')

# 3. Корреляция между возрастом пользователей и их оценками
correlation = np.corrcoef(rating_user['Age'], rating_user['Rating'])[0, 1]
print(f"Корреляция между возрастом и оценками: {correlation}")





