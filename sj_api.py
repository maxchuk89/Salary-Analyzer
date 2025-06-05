import os
import requests
from dotenv import load_dotenv

from salary_prediction import predict_salary_from_range
from salary_table import print_salary_table

load_dotenv()
SUPERJOB_API_KEY = os.getenv('SUPERJOB_API_KEY')

SJ_DEVELOPMENT_CATALOGUE_ID = 48
SJ_PAGE_SIZE = 100


def fetch_all_vacancies(language, api_key, catalogue_id, page_size):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': api_key}
    page = 0
    vacancies = []

    while True:
        params = {
            'keyword': f'Программист {language}',
            'town': 'Москва',
            'catalogues': catalogue_id,
            'count': page_size,
            'page': page
        }
        reply = requests.get(url, headers=headers, params=params, timeout=10)
        reply.raise_for_status()
        response = reply.json()

        vacancies.extend(response['objects'])

        if not response['more']:
            break

        page += 1

    return vacancies, response['total']


def predict_rub_salary_for_superJob(vacancy):
    if vacancy['currency'] != 'rub':
        return None

    start = vacancy['payment_from']
    end = vacancy['payment_to']

    return predict_salary_from_range(start, end)


def calculate_average_salaries_superjob(languages, api_key, catalogue_id, page_size):
    statistics = {}

    for language in languages:
        vacancies, found = fetch_all_vacancies(language, api_key, catalogue_id, page_size)

        salaries = [
            predict_rub_salary_for_superJob(vacancy)
            for vacancy in vacancies
        ]
        valid_salaries = [salary for salary in salaries if salary]

        if valid_salaries:
            average_salary = int(sum(valid_salaries) / len(valid_salaries))
        else:
            average_salary = 0

        statistics[language] = {
            'vacancies_found': found,
            'vacancies_processed': len(valid_salaries),
            'average_salary': average_salary
        }

    return statistics


if __name__ == '__main__':
    languages = ['Python', 'Java', 'C++', 'C#', 'JavaScript', 'Ruby', 'Go', '1C']
    stats = calculate_average_salaries_superjob(
        languages,
        SUPERJOB_API_KEY,
        SJ_DEVELOPMENT_CATALOGUE_ID,
        SJ_PAGE_SIZE
    )
    print_salary_table(stats, 'SuperJob Moscow')
