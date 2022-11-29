import requests
from bs4 import BeautifulSoup as BSop
import time
from datetime import datetime, timedelta
import pandas as pd
# version 0.2.0


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
    merged_list = [(([names[i]])+(values[i*number_of_values:(i*number_of_values)+number_of_values]))
                   for i in range(len(names))]
    return merged_list


def calculate_years_between(date1, date2):
    try:
        number_of_indywidual_years = int(
            date2.strftime("%Y"))-int(date1.strftime("%Y"))
        return number_of_indywidual_years+1
    except AttributeError:
        return 0


def marge_csv_files(year, delate=False):
    months = ['01', '02', '03', '04', '05',
              '06', '07', '08', '09', '10', '11', '12']
    csv_list = ['GPW_{}-{}.csv'.format(year, nr) for nr in months]
    df_end = pd.concat(
        map(pd.read_csv, csv_list), ignore_index=True)
    df_end.to_csv(("{}{}{}").format('GPW_', year, '.csv'),
                  index=False, encoding='utf-8')
    print('{}{}{}{}'.format('Saved as: ', 'GPW_', year, '.csv'))
    if delate:
        print('Sub files delated')
        # delate file


def scrap_and_convert_into_csv():
    years_range = [2014]
    # (2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000)
    for year in years_range:
        start_time = time.time()
        staring_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        date_to_loop = staring_date
        range_of_days = (end_date-staring_date).days

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
        month = 1
        start_time_for_month = time.time()
        for day in range(range_of_days+1):
            print('month: ', int(date_to_loop.strftime("%m")), month,
                  ' /12 _ ', day+1, '/', range_of_days+1)
            soup = BSop(get_data_from_gpw_link(
                date_to_loop).text, 'html.parser')
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
            if month != int(date_to_loop.strftime("%m")):
                df.to_csv(("{}{}{}").format('GPW_', (date_to_loop-timedelta(days=1)).strftime("%Y-%m"), '.csv'),
                          header=df.columns, index=False, encoding='utf-8')
                df = df.iloc[0:0]
                df = pd.DataFrame(columns=gpw_columns)
                row = row.iloc[0:0]
                row = pd.DataFrame(columns=gpw_columns)
                print('Saved, this month: ', (time.time()-start_time_for_month))
                month += 1
                start_time_for_month = time.time()

        marge_csv_files(year)
        print('Total time spend for this year: ', time.time()-start_time)


App_run = True
if App_run:
    scrap_and_convert_into_csv()
