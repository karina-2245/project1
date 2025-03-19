import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#импортируем три дата сета с информацией о фильмах, их рейтинге, и пользователях стриминг-сервиса
movies_data = pd.read_csv('/Users/grigorovakarina/Downloads/archive/Netflix_Dataset_Movie.csv')
ratings = pd.read_csv('/Users/grigorovakarina/Downloads/archive/Netflix_Dataset_Rating.csv')
users = pd.read_csv('/Users/grigorovakarina/Downloads/netflix_users.csv')

#проверим все три дата сета на наличие пустых значений
print(movies_data.isnull().sum())

print(ratings.isnull().sum())

print(users.isnull().sum())

#заполним пустые значения
ratings['Rating'] = ratings['Rating'].fillna(ratings['Rating'].mean())
users['Age'] = users['Age'].fillna(users['Age'].median())

#объединим таблицы movie_data и movies_ratings:
merged_df = pd.merge(movies_data, ratings, on = 'Movie_ID')
rating_user = pd.merge(users, merged_df, on = 'User_ID')
print(rating_user.head())

#Аналитические запросы
#1. Самый популярный жанр
#разделяю колонку Favorite_Genre, на случай, если у фильма несколько жанров
rating_user = rating_user.assign(Genres=rating_user['Favorite_Genre'].str.split('|')).explode('Favorite_Genre')
#считаю кол-во и нахожу максимальное
most_popular_genre = rating_user['Favorite_Genre'].value_counts().idxmax()
print(f'Самый популярный жанр среди пользователей:\n{most_popular_genre}')

#1.2 Самый популярный жанр для возрастных групп
#Создаем колонку Age_Group
rating_user['Age_Group'] = pd.cut(rating_user['Age'],
                                  bins = [18,30,45,60,90],
                                  labels= ['18-30', '30-45', '45-60', '60-90'])
print(rating_user.head())
#Создаем сводную таблицу: абсцисса Favorite Genre, ордината Age_Group, значение Rating как среднее
pivot = pd.pivot_table(rating_user,
                    index = 'Favorite_Genre',
                    columns = 'Age_Group',
                    aggfunc = 'mean',
                    values = 'Rating')
print(f'Сводная таблица:\n {pivot.round(2)}')
#нахожу максимальный средний рейтинг по каждому столбцу в сводной таблице
popular_genre = pivot.idxmax(axis=0)
#создаю новый DataFrame:
popular_genre_df = popular_genre.reset_index()
popular_genre_df.columns = ['Age_Group', 'Most_Popular_Genre']
print(f'Самый популярный жанр для каждой возрастной группы:\n{popular_genre_df}')

#2. Средний рейтинг фильмов за каждое десятилетие
bins1=[1960, 1970, 1980, 1990, 2000]
#создание нового столбца Decade
rating_user['Decade'] = pd.cut(
    rating_user['Year'],
    bins=bins1,
    right=False,
    labels=[f'{bins1[i]}' for i in range(len(bins1) - 1)])
#группировка по Decade и нахождение среднего рейтинга
avg_rating_by_year = round(rating_user.groupby('Decade')['Rating'].mean(),2)
print(f'Средний рейтинг фильмов за каждое десятилетие:\n{avg_rating_by_year}')

#3. Корреляция между возрастом пользователей и их оценками
correlation = np.corrcoef(rating_user['Age'], rating_user['Rating'])[0, 1]
print(f"Корреляция между возрастом и оценками: {correlation}")

#4. Страна с наибольшим кол-вом пользователей
country_most_users = rating_user['Country'].value_counts().idxmax()
print(f'Страна с наибольшим кол-вом пользователей:\n{country_most_users}')

#5. Самый популярный жанр в каждой стране
#группировка по стране, к жанру применяем формулу: нахождение моды
top_genre_by_country = rating_user.groupby('Country')['Favorite_Genre'].apply(lambda x: x.mode()[0])
print(f'Самый популярный жанр в каждой стране:\n {top_genre_by_country}')

#6. Отбор фильмов с рейтингом больше 4,5 (булевая индексация + маскировка)
top_movies = rating_user[rating_user['Rating'] > 4.5][['Movie_ID', 'Rating']]
print(top_movies)

#7. Количество просмотренный часов для каждого типа подписки:
watch_hours = rating_user.groupby('Subscription_Type', observed=True)['Watch_Time_Hours'].sum()
print(f'Количество просмотренный часов для каждого типа подписки:\n{watch_hours}')

#Визуализация
#1 Гистограмма распределения возраста пользователей
sns.histplot(rating_user['Age'], bins = 10, kde = True, color='pink')
plt.title('Распределение возраста пользователей')
plt.show()

#2 Кривая плотности рейтинга
sns.kdeplot(rating_user['Rating'], color='blue', fill=True)
plt.title('Кривая плотности рейтинга')
plt.show()

#3 Гистограмма количества каждого типа подписки для каждой возрастной группы
#сгруппируем данные по возрастной группе и типу подписки,
subscription_counts = rating_user.groupby(['Age_Group', 'Subscription_Type'], observed=True).size().reset_index(name='Count')

# Построение barplot
sns.barplot(x='Age_Group', y='Count', hue='Subscription_Type', data=subscription_counts, palette='viridis')
plt.title('Распределение типов подписок по возрастным группам')
plt.xlabel('Возрастная группа')
plt.ylabel('Количество подписок')
plt.legend(title='Тип подписки')
plt.show()







