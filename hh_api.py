import os
import requests

from salary_prediction import predict_salary_from_range


HH_API_URL = 'https://api.hh.ru/vacancies'
HH_PAGE_SIZE = 100
HH_SEARCH_PERIOD = 30
HH_MOSCOW_AREA_ID = 1


def fetch_vacancies(language):
    vacancies = []
    page = 0

    while True:
        params = {
            'text': f'Программист {language}',
            'area': HH_MOSCOW_AREA_ID,
            'period': HH_SEARCH_PERIOD,
            'per_page': HH_PAGE_SIZE,
            'page': page
        }
        reply = requests.get(HH_API_URL, params=params, timeout=10)
        reply.raise_for_status()
        response = reply.json()

        vacancies += response['items']

        if page >= response['pages'] - 1:
            break

        page += 1

    return vacancies, response['found']


def predict_rub_salary(vacancy):
    if vacancy['salary'] is None:
        return None
    if vacancy['salary']['currency'] != 'RUR':
        return None

    start = vacancy['salary']['from']
    end = vacancy['salary']['to']

    return predict_salary_from_range(start, end)


def calculate_average_salaries(languages):
    statistics = {}

    for language in languages:
        vacancies, total_found = fetch_vacancies(language)

        salaries = [
            predict_rub_salary(vacancy)
            for vacancy in vacancies
        ]
        valid_salaries = [salary for salary in salaries if salary]

        if valid_salaries:
            average_salary = int(sum(valid_salaries) / len(valid_salaries))
        else:
            average_salary = 0

        statistics[language] = {
            'vacancies_found': total_found,
            'vacancies_processed': len(valid_salaries),
            'average_salary': average_salary
        }

    return statistics
