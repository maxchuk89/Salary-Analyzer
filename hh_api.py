import requests
from salary_prediction import predict_salary_from_range

MOSCOW_AREA_ID = 1
SEARCH_PERIOD_DAYS = 30
HH_PAGE_SIZE = 100


def fetch_vacancies(language):
    url = 'https://api.hh.ru/vacancies'
    vacancies = []
    page = 0

    while True:
        params = {
            'text': f'Программист {language}',
            'area': MOSCOW_AREA_ID,
            'period': SEARCH_PERIOD_DAYS,
            'per_page': HH_PAGE_SIZE,
            'page': page
        }
        reply = requests.get(url, params=params, timeout=10)
        reply.raise_for_status()
        page_data = reply.json()

        vacancies.extend(page_data['items'])

        if page >= page_data['pages'] - 1:
            break

        page += 1

    return vacancies, page_data['found']


def predict_rub_salary(vacancy):
    salary = vacancy.get('salary')
    if not salary or salary.get('currency') != 'RUR':
        return None

    start = salary.get('from')
    end = salary.get('to')
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
