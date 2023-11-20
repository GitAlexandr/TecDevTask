import requests
from bs4 import BeautifulSoup


def parse_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    person_name = soup.find('h1', {'class': 'page-title__title'}).text.strip()
    html_code = str(soup)
    return {'url': url, 'name': person_name, 'html_code': html_code}