import csv
from typing import Dict, Optional


def print_departments(csv_reader):
    departments = set()
    for row in csv_reader:
        # KeyError
        departments.add(row['Отдел'])
    print('Список отделов:')
    for department in departments:
        print(department)


def create_summary_report(csv_reader: csv.DictReader) -> Dict[str, Dict[str, int]]:
    departments_stats = dict()
    for row in csv_reader:
        department_name = row['Отдел']
        salary = int(row['Оклад'])
        departments_stats.setdefault(department_name,
                                     {'min_salary': None, 'max_salary': None, 'staff_number': 0,
                                      'salary_sum': 0})
        current_department_stats = departments_stats[department_name]
        if current_department_stats['max_salary'] is None or salary > current_department_stats[
            'max_salary']:
            current_department_stats['max_salary'] = salary
        if current_department_stats['min_salary'] is None or salary < current_department_stats[
            'min_salary']:
            current_department_stats['min_salary'] = salary
        current_department_stats['salary_sum'] += salary
        current_department_stats['staff_number'] += 1
    for department in departments_stats:
        current_department_stats = departments_stats[department]
        current_department_stats['mean_salary'] = current_department_stats['salary_sum'] / \
                                                  current_department_stats[
                                                      'staff_number']  # zero division
    return departments_stats


def print_summary_report(report: Dict[str, Dict[str, int]], output_filename: Optional[str] = None):
    print(report)
    pass


def choose_option(options_number: int) -> int:
    while True:
        try:
            option = int(input())
            if option in range(options_number):
                return option
        except ValueError:
            print(f'Incorrect input, try again. Choose number from 0 to {options_number - 1}')


def main():
    input_filename = 'funcs_homework_employees_sample.csv'
    output_filename = 'report.csv'
    delimiter = ';'

    options_descriptions = (
        'Показать список отделов', 'Показать сводный отчет', 'Сохранить сводный отчет')
    print("Выберите:\n" + "\n".join(
        f"{i}) {description}" for i, description in enumerate(options_descriptions)))
    options_number = len(options_descriptions)
    option = choose_option(options_number)

    with open(input_filename) as f:
        info = csv.DictReader(f, delimiter=delimiter)

        # TODO: errors for no file and incorrect csv
        if option == 0:
            print_departments(info)
        elif option == 1:
            report = create_summary_report(info)
            print_summary_report(report)
        elif option == 2:
            report = create_summary_report(info)
            print_summary_report(report, output_filename)
        else:
            pass


if __name__ == '__main__':
    main()
