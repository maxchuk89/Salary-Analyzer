import os
import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable

load_dotenv()

SJ_DEVELOPMENT_CATALOGUE_ID = 48
SJ_PAGE_SIZE = 100

superjob_key = os.getenv('SUPERJOB_API_KEY')


def fetch_all_vacancies(language):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': superjob_key}
    page = 0
    vacancies = []

    while True:
        params = {
            'keyword': f'Программист {language}',
            'town': 'Москва',
            'catalogues': SJ_DEVELOPMENT_CATALOGUE_ID,
            'count': SJ_PAGE_SIZE,
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


def predict_salary_from_range(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8
    return None


def predict_rub_salary_for_superJob(vacancy):
    if vacancy['currency'] != 'rub':
        return None

    start = vacancy['payment_from']
    end = vacancy['payment_to']

    return predict_salary_from_range(start, end)


def calculate_average_salaries_superjob(languages):
    statistics = {}

    for language in languages:
        vacancies, found = fetch_all_vacancies(language)

        salaries = [
            predict_rub_salary_for_superJob(vacancy)
            for vacancy in vacancies
        ]
        filtered = [salary for salary in salaries if salary]

        if filtered:
            average = int(sum(filtered) / len(filtered))
        else:
            average = 0

        statistics[language] = {
            'vacancies_found': found,
            'vacancies_processed': len(filtered),
            'average_salary': average
        }

    return statistics


def print_salary_table(statistics, title):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]

    for language, info in statistics.items():
        row = [
            language,
            info['vacancies_found'],
            info['vacancies_processed'],
            info['average_salary']
        ]
        table_data.append(row)

    table = AsciiTable(table_data, title)
    print(table.table)


if __name__ == '__main__':
    languages = ['Python', 'Java', 'C++', 'C#', 'JavaScript', 'Ruby', 'Go', '1C']
    stats = calculate_average_salaries_superjob(languages)
    print_salary_table(stats, 'SuperJob Moscow')
