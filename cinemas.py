import requests
from bs4 import BeautifulSoup


def fetch_response(url, params=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Mobile; rv:15.0) Gecko/15.0 Firefox/15.0'
    }
    return requests.get(
        url,
        headers=headers,
        params=params,
    )


def parse_afisha_info(html_page):
    soup = BeautifulSoup(html_page, 'html.parser')
    return [
        dict(
            title=movie.h3.a.string,
            cinemas=len(movie.find_all('td', class_='b-td-item')),
        )
        for movie in soup.find_all('div', class_='s-votes-hover-area')
    ]


def parse_kinopoisk_info(json_content):
    rate = json_content['page']['suggest']['items']['movies'][0]['ratings']
    if rate is None:
        return dict(rating=0.0, votes='0')
    return dict(
        rating=(
            float(rate['kp']['value'])
            if rate['kp']['isReady'] else 0.0
        ),
        votes=str(rate['kp']['count'])
    )


def prepare_movies(min_cinema_count=10):
    afisha_page = fetch_response(
        'https://www.afisha.ru/msk/schedule_cinema/'
    ).text
    movies = []
    for afisha_item in parse_afisha_info(afisha_page):
        if afisha_item['cinemas'] >= min_cinema_count:
            kinopoisk_json = fetch_response(
                'https://www.kinopoisk.ru/search/suggest/',
                params={'value': afisha_item['title']}
            ).json()
            kinopoisk_item = parse_kinopoisk_info(kinopoisk_json)
            movies.append({**afisha_item, **kinopoisk_item})
    return sorted(movies, key=lambda k: k['rating'], reverse=True)


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
    output_table_to_console(table=movies)
