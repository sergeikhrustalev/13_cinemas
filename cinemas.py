import requests
from bs4 import BeautifulSoup


def fetch_afisha_page():
    
    afisha_page = 'https://www.afisha.ru/msk/schedule_cinema/'    
    
    return requests.get(afisha_page).content


def parse_afisha_list(raw_html):
    
    soup = BeautifulSoup(html, 'html.parser')
    
    return [
        
        dict(
            movie_title=movie.h3.a.string,
            cinema_count=len(movie.find_all('td', class_='b-td-item')),
        )
        
        for movie in soup.find_all('div', class_='s-votes-hover-area')
        
    ]


def fetch_movie_info(movie_title):
    pass


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    
    
    html = fetch_afisha_page()
    
    print(parse_afisha_list(html))
    
    
    
    
    
