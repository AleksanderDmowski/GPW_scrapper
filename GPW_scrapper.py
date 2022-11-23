import requests
from bs4 import BeautifulSoup as BSop
import time
from datetime import datetime, timedelta
import pandas as pd
# version 0.1.0


def get_data_from_gpw_link(date):
    res = requests.get(
        'https://www.gpw.pl/archiwum-notowan-full?type=10&instrument=&date={}'.format(date.strftime("%d-%m-%Y")))
    return res


def create_names_list_from_data(names):
    nameslist = []
    i = 0
    for name in range(round((len(names)-2)/2)):
        nameslist.append((names[i+2]).getText())
        i += 2
    return nameslist


def create_values_list_from_data(numbers):
    cleared_page = []
    cleared_values = []

    for nr in numbers:
        cleared_page.append(nr.getText().replace(
            '\xa0', '').replace('\n', '').replace(' ', ''))

    for value in cleared_page:
        if value.find(",") != -1 or value.isnumeric():
            cleared_values.append(value)

    return cleared_values


def merge_lists(names, values):
    number_of_values = 8
    merged_list = []
    for postion in range(len(names)):
        merged_list += [[names[postion], *
                         values[(postion*number_of_values):((postion*number_of_values)+number_of_values)]]]
    return merged_list


def scrap_and_convert_into_csv():
    staring_date = datetime(2022, 11, 21)
    end_date = datetime(2022, 11, 21)
    start_time = time.time()
    date_to_loop = staring_date
    range_of_dates = (end_date-staring_date).days
    gpw_columns = [
        'Nazwa spółki',
        'Kurs otwarcia',
        'Kurs min',
        'Kurs max',
        'Kurs zamknięcia',
        'Zmiana kursu w procent',
        'Wolumen obrotu w szt',
        'Lista transkacji',
        'Wartość obrotu w tys',
        'Dzień']
    df = pd.DataFrame(columns=gpw_columns)
    row = pd.DataFrame(columns=gpw_columns)
    for day in range(range_of_dates+1):
        print(date_to_loop)
        soup = BSop(get_data_from_gpw_link(date_to_loop).text, 'html.parser')
        names = soup.select('.left')
        values = soup.select('.text-right')
        data_list_for_loop = merge_lists(create_names_list_from_data(
            names), create_values_list_from_data(values))
        if len(data_list_for_loop) != 0:
            for record in data_list_for_loop:
                record.append(("{}").format(date_to_loop))
                row.loc[len(row)] = record
                df = pd.concat([row], axis=0)

        date_to_loop += timedelta(days=1)

    df.to_csv(("{}").format('custom_file_name.csv'),
              header=df.columns, index=False, encoding='utf-8')
    print(time.time()-start_time)


scrap_and_convert_into_csv()
