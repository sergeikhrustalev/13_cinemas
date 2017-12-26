import requests
from bs4 import BeautifulSoup


def fetch_afisha_page():

    return requests.get(
        'https://www.afisha.ru/msk/schedule_cinema/'
    ).text


def parse_afisha_list(raw_html):

    soup = BeautifulSoup(raw_html, 'html.parser')

    return [

        dict(
            movie_title=movie.h3.a.string,
            cinema_count=len(movie.find_all('td', class_='b-td-item')),
        )

        for movie in soup.find_all('div', class_='s-votes-hover-area')

    ]


def fetch_movie_info(movie_title):

    headers = {
        'Accept-Language': 'ru',
        'Host': 'www.kinopoisk.ru',
        'Referer': 'https://www.kinopoisk.ru/',
        'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'
    }

    movie_page = requests.get(
        'https://www.kinopoisk.ru/index.php',
        headers=headers,
        params=dict(kp_query=movie_title),
        timeout=10
    ).text

    soup = BeautifulSoup(movie_page, 'html.parser')

    return dict(

        movie_rating=soup.find(
            'span',
            class_='movie-snippet__rating-value'
        ).string,

        votes_count=soup.find(
            'span',
            class_='movie-snippet__rating-votes'
        ).string,

    )

def output_movies_to_console(movies):
    pass


if __name__ == '__main__':

    html = fetch_afisha_page()

    total = [
        
        dict(
            
            list(afisha_item.items()) + list(fetch_movie_info(afisha_item['movie_title']).items())
        )

        for afisha_item in parse_afisha_list(html)
        if afisha_item['cinema_count'] > 10

    ]

    print(total)

