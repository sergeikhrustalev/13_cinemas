import requests
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


def fetch_movie_info(title):

    headers = {

        'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'
    }

    rate_info = requests.get(
        'https://www.kinopoisk.ru/search/suggest/',
        headers=headers,
        params=dict(value=title),
    ).json()['page']['suggest']['items']['movies'][0]['ratings']['kp']

    return dict(

        rating=float(rate_info['value']) if rate_info['isReady'] else 0.0,

        votes=str(rate_info['count'])
        
    )


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':

    html = fetch_afisha_page()

    total = [
        
        dict(
            
            list(
                afisha_item.items()
            ) + 
            
            list(
                fetch_movie_info(afisha_item['title']).items()
            )
        )

        for afisha_item in parse_afisha_list(html)
        if afisha_item['cinemas'] > 20

    ]

    print(total)
