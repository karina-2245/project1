import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#импортируем три дата сета с информацией о фильмах, их рейтинге, и пользователях стриминг-сервиса
movies = pd.read_csv('/Users/grigorovakarina/Downloads/archive/Netflix_Dataset_Movie.csv')
movies_ratings = pd.read_csv('/Users/grigorovakarina/Downloads/archive/Netflix_Dataset_Rating.csv')
users = pd.read_csv('/Users/grigorovakarina/Downloads/netflix_users.csv')

#проверим все три дата сета на наличие пустых значений
print(movies, isnull())
print(movies_ratings, isnull())
print(users, isnull())

