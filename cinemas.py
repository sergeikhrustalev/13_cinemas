import requests
import time
from bs4 import BeautifulSoup


def get_response(url, params=None, wait_sec=2):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Mobile; rv:15.0) Gecko/15.0 Firefox/15.0'
    }

    time.sleep(wait_sec)

    return requests.get(
        url,
        headers=headers,
        params=params,
    )


def get_afisha_info():

    soup = BeautifulSoup(
        get_response('https://www.afisha.ru/msk/schedule_cinema/').text,
        'html.parser'
    )

    return [

        dict(
            title=movie.h3.a.string,
            cinemas=len(movie.find_all('td', class_='b-td-item')),
        )

        for movie in soup.find_all('div', class_='s-votes-hover-area')

    ]


def get_kinopoisk_info(movie_title):

    rate_info = get_response(
        'https://www.kinopoisk.ru/search/suggest/',
        params=dict(value=movie_title),
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


def prepare_movies(min_cinema_count=10):

    return sorted(

        [

            dict(

                list(
                    afisha_item.items()
                ) +

                list(
                    get_kinopoisk_info(afisha_item['title']).items()
                )

            )

            for afisha_item in get_afisha_info()
            if afisha_item['cinemas'] >= min_cinema_count

        ],

        key=lambda k: k['rating'],

        reverse=True,

    )


def output_table_to_console(table, rows_count=10):

    print(

        '{:50}{:6} {:>10}{:>10}'.format(
            'TITLE',
            'RATING',
            'VOTES',
            'CINEMAS',
        )

    )

    for row in table[:rows_count]:

        print(

            '{:50}{:6} {:>10}{:>10}'.format(
                row['title'],
                row['rating'],
                row['votes'],
                row['cinemas'],
            )

        )


if __name__ == '__main__':

    movies = prepare_movies()

    output_table_to_console(
        table=movies
    )
