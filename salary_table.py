from terminaltables import AsciiTable


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
