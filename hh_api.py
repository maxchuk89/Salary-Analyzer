import requests
from terminaltables import AsciiTable


def fetch_vacancies(language):
    url = 'https://api.hh.ru/vacancies'
    vacancies = []
    page = 0

    while True:
        params = {
            'text': f'Программист {language}',
            'area': 1,
            'period': 30,
            'per_page': 100,
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

    if start and end:
        return (start + end) / 2
    if start:
        return start * 1.2
    if end:
        return end * 0.8

    return None


def calculate_average_salaries(languages):
    statistics = {}

    for language in languages:
        vacancies, total_found = fetch_vacancies(language)

        salaries = [
            predict_rub_salary(vacancy)
            for vacancy in vacancies
        ]
        filtered = [salary for salary in salaries if salary is not None]

        if filtered:
            average = int(sum(filtered) / len(filtered))
        else:
            average = 0

        statistics[language] = {
            'vacancies_found': total_found,
            'vacancies_processed': len(filtered),
            'average_salary': average
        }

    return statistics


def print_salary_table(statistics, title):
    table_data = [
        ['Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата']
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
    stats = calculate_average_salaries(languages)
    print_salary_table(stats, 'HeadHunter Moscow')