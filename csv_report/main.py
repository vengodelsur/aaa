import csv
import sys
from typing import Dict, Optional, TextIO, Tuple


def print_departments(csv_reader: csv.DictReader):
    """
    Печатает список отделов, встретившихся в csv
    :param csv_reader: объект для чтени информации об отделах из csv
    """
    departments = set()
    for row in csv_reader:
        # KeyError
        departments.add(row['Отдел'])
    print('Список отделов:')
    for department in departments:
        print(department)


def create_summary_report(csv_reader: csv.DictReader) -> Dict[str, Dict[str, int]]:
    """
    Создаёт отчёт о минимальной, максимальной, средней зарплате по отделам :param csv_reader:
    объект для чтени информации об отделах из csv
    :return: словарь со сводной информацией о зарплате по отделам, например:
        {'Продажи': {'department_name': 'Продажи', 'min_salary': 100500, 'max_salary': 100500,
                     'mean_salary': 100500.0,'staff_number': 1, 'salary_sum': 100500}}
    """

    departments_stats = dict()
    for row in csv_reader:
        department_name = row['Отдел']
        salary = int(row['Оклад'])
        departments_stats.setdefault(department_name,
                                     {'department_name': department_name, 'min_salary': None,
                                      'max_salary': None, 'staff_number': 0, 'salary_sum': 0})
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
    """
    Выводит/сохраняет отчёт о минимальной, максимальной, средней зарплате по отделам
    :param report: словарь с информацией по отделам, например:
        {'Продажи': {'department_name': 'Продажи', 'min_salary': 100500, 'max_salary': 100500,
                     'mean_salary': 100500.0}}
    :param output_filename: имя файла для вывода отчета (если None, используется стандартный вывод)
    :return:
    """
    keys = ('department_name', 'min_salary', 'max_salary', 'mean_salary')
    if output_filename is None:
        report_to_csv(report, keys, sys.stdout)
        return
    with open(output_filename, 'w') as f:
        report_to_csv(report, keys, f)


def report_to_csv(report: Dict[str, Dict[str, int]], keys: Tuple[str, ...], f: TextIO,
                  delimiter: Optional[str] = '\t'):
    """
    Форматирует в csv и записывает отчёт
    :param report: словарь с информацией по отделам, например:
        {'Продажи': {'department_name': 'Продажи', 'min_salary': 100500, 'max_salary': 100500,
                     'mean_salary': 100500.0}}
    :param keys: ключи, которые нужно использовать из словаря с информацией, например:
        ('department_name', 'min_salary', 'max_salary', 'mean_salary')
    :param f: TextIO объект - куда записывать csv
    :param delimiter: разделитель
    """
    dict_writer = csv.DictWriter(f, keys, delimiter=delimiter)
    dict_writer.writeheader()
    for department_stats in report.values():
        dict_writer.writerow({key: department_stats[key] for key in keys})


def choose_option(options_number: int) -> int:
    """
    Запрашивает у пользователя порядковый номер пункта меню (с проверкой корректности ввода)
    :param options_number: количество пунктов в меню
    :return: номер выбранного пользователем пункта меню
    """
    while True:
        try:
            option = int(input())
            if option in range(options_number):
                return option
        except ValueError:
            print(f'Incorrect input, try again. Choose number from 0 to {options_number - 1}')


def main():
    """
    По выбору пользователя выводит информацию из v отчёта о сотрудниках компании:
    выводит список отделов
    выводит сводный отчёт (минимальная, максимальная, средняя зарплата по отделам)
    сохраняет сводный отчёт в файл (минимальная, максимальная, средняя зарплата по отделам)
    """
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
