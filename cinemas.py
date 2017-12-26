import requests
import time
from bs4 import BeautifulSoup


def fetch_afisha_page():

    return requests.get(
        'https://www.afisha.ru/msk/schedule_cinema/'
    ).text


def parse_afisha_list(html):

    soup = BeautifulSoup(html, 'html.parser')

    return [

        dict(
            title=movie.h3.a.string,
            cinemas=len(movie.find_all('td', class_='b-td-item')),
        )

        for movie in soup.find_all('div', class_='s-votes-hover-area')

    ]


def fetch_movie_info(title, waiting_sec=6):

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


def prepare_movies_data(min_cinema_count=20):

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

            for afisha_item in parse_afisha_list(fetch_afisha_page())
            if afisha_item['cinemas'] >= min_cinema_count

        ],

        key=lambda k: k['rating'],

        reverse=True,

    )


if __name__ == '__main__':
    print(prepare_movies_data())
