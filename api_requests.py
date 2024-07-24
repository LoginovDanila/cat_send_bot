import requests
import logging

URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_image():
    try:
        response = requests.get(URL).json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = plan_b()
    random_animal = response[0].get('url')
    return random_animal


def plan_b():
    new_url = 'https://api.thedogapi.com/v1/images/search'
    return requests.get(new_url).json()
