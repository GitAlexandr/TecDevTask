import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import time

import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import time

def parse_data(url):
    retry_attempts = 3
    current_attempt = 0

    while current_attempt < retry_attempts:
        try:
            user_agent_rotator = UserAgent(software_names=[SoftwareName.CHROME.value], operating_systems=[OperatingSystem.WINDOWS.value], limit=100)
            headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            person_name = soup.find('h1', {'class': 'page-title__title'}).text.strip()
            html_code = str(soup)
            return {'url': url, 'name': person_name, 'html_code': html_code}

        except requests.exceptions.RequestException as e:
            if current_attempt == retry_attempts - 1 or response.status_code != 429:
                print(f"Failed to fetch data from {url}: {e}")
                return None

            print(f"Received 429 error. Retrying attempt {current_attempt + 1} with a different user agent...")
            headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
            time.sleep(5 * (current_attempt + 1))  # Increase the delay between retries
            current_attempt += 1

    print(f"All retry attempts failed. Unable to fetch data from {url}.")
    return None


