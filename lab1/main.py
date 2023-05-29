import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top'

response = requests.get(url) # Отправка GET-запроса и получение содержимого страницы
content = response.content

soup = BeautifulSoup(content, 'html.parser') # Создание объекта для парсинга HTML-контента

movie_elements = soup.select('td.titleColumn')
rating_elements = soup.select('td.imdbRating strong')

movies_dict = {} # Словарь

for index, element in enumerate(movie_elements[:250]): # Добавление их в словарь
    movie_title = element.a.text
    movie_rank = element.text.split('.')[0].strip() # Удаление пробельных символов
    movie_rating = rating_elements[index].text
    movies_dict[movie_title] = {
        'Rank': int(movie_rank),
        'Rating': float(movie_rating)
    }

for movie_title, movie_info in movies_dict.items():
    print(f"{movie_info['Rank']}. {movie_title} - Rating: {movie_info['Rating']}")

