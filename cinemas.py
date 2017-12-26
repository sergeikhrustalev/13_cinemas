import requests
import time
from bs4 import BeautifulSoup


def fetch_afisha_page():

    return requests.get(
        'https://www.afisha.ru/msk/schedule_cinema/'
    ).text


def get_afisha_list(html):

    soup = BeautifulSoup(html, 'html.parser')

    return [

        dict(
            title=movie.h3.a.string,
            cinemas=len(movie.find_all('td', class_='b-td-item')),
        )

        for movie in soup.find_all('div', class_='s-votes-hover-area')

    ]


def fetch_movie_info(title, waiting_sec=3):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Mobile; rv:15.0) Gecko/15.0 Firefox/15.0'
    }

    time.sleep(waiting_sec)

    rate_info = requests.get(
        'https://www.kinopoisk.ru/search/suggest/',
        headers=headers,
        params=dict(value=title)
    ).json()['page']['suggest']['items']['movies'][0]['ratings']

    if rate_info is None:
        return dict(rating=0.0, votes='0')

    return dict(

        rating=(
            float(rate_info['kp']['value'])
            if rate_info['kp']['isReady'] else 0.0
        ),

        votes=str(rate_info['kp']['count'])

    )


def prepare_movies_data(min_cinema_count=10):

    return sorted(

        [

            dict(

                list(
                    afisha_item.items()
                ) +

                list(
                    fetch_movie_info(afisha_item['title']).items()
                )

            )

            for afisha_item in get_afisha_list(fetch_afisha_page())
            if afisha_item['cinemas'] >= min_cinema_count

        ],

        key=lambda k: k['rating'],

        reverse=True,

    )


def output_data_to_console():

    count = 10

    movies_items = prepare_movies_data()[:count]

    print(

        '{:50}{:6} {:>10}{:>10}'.format(
            'TITLE',
            'RATING',
            'VOTES', 
            'CINEMAS',
        )

    )

    for movies_item in movies_items:

        print(

            '{:50}{:6} {:>10}{:>10}'.format(
                movies_item['title'],
                movies_item['rating'],
                movies_item['votes'],
                movies_item['cinemas'],
            )

        )


if __name__ == '__main__':
    output_data_to_console()
