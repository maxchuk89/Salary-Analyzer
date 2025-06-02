from hh_api import calculate_average_salaries as calculate_hh
from sj_api import calculate_average_salaries_superjob as calculate_sj
from sj_api import print_salary_table


if __name__ == '__main__':
    languages = ['Python', 'Java', 'C++', 'C#', 'JavaScript', 'Ruby', 'Go', '1C']

    hh_stats = calculate_hh(languages)
    print_salary_table(hh_stats, 'HeadHunter Moscow')

    print()  # пустая строка

    sj_stats = calculate_sj(languages)
    print_salary_table(sj_stats, 'SuperJob Moscow')
