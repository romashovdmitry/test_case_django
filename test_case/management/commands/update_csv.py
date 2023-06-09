# Django packages
from django.core.management import BaseCommand

# custom Django classes
from test_case.models import Region, Operator, PhoneNumber

# libs for download CSV
from bs4 import BeautifulSoup
import requests
import urllib3
import re
import pandas
import os

# import SQL transactions by cursor
from test_case.transactions import SQLTransactions


def download_csv_helper() -> None:

    url = 'https://opendata.digital.gov.ru/registry/numeric/downloads/'

    # eroor with reqeust resolving
    # https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
    requests.packages.urllib3.disable_warnings()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # get DOM of page
    page = requests.get(url=url, verify=False)

    # get list of <a> tags from DOM
    soup = BeautifulSoup(page.text, "html.parser")
    soup = soup.find_all('a')

    for link in soup:

        if link.get('class') == ['text-primary-500', 'hover:text-primary-600']:

            csv_name = link.get('href')
            csv_name = csv_name.replace(
                'https://opendata.digital.gov.ru/downloads/', '')
            csv_name = re.sub(r'\?\S+', '', csv_name)

            csv_obj = requests.get(url=link.get('href'), verify=False)
            open(f'{csv_name}', 'wb').write(csv_obj.content)


def create_csv_helper() -> list:

    csv_names = []

    # delete all CSV from local
    os_list = os.listdir(os.getcwd())
    for os_file in os_list:
        if '.csv' in os_file:
            os.remove(os_file)

    # clean DB
    SQLTransactions().delete_all_data()

    # download CSV
    download_csv_helper()

    # get names of downloaded CSV
    os_list = os.listdir(os.getcwd())
    for os_file in os_list:
        if '.csv' in os_file:
            csv_names.append(os_file)
    return csv_names


def insert_phone_number(pandas_obj):

    bulk_list = []

    step = 5000

    for index, row in pandas_obj.iterrows():
        if index < (step-1):
            region_fk = Region.objects.filter(geo=row.Регион).filter(
                city_code=row['АВС/ DEF']).first()
            operator = Operator.objects.get(operator=row.Оператор)
            bulk_list.append(
                PhoneNumber(
                    start=row.От,
                    finish=row.До,
                    region=region_fk,
                    operator=operator
                )
            )
        else:
            step += 5000
            PhoneNumber.objects.bulk_create(bulk_list)
            bulk_list = []
    if bulk_list != []:
        PhoneNumber.objects.bulk_create(bulk_list)


def insert_operator(pandas_obj):

    bulk_list = []

    operators = list(dict.fromkeys(pandas_obj['Оператор']))

    for operator in operators:
        bulk_list.append(
            Operator(
                operator=operator
            )
        )

    Operator.objects.bulk_create(bulk_list, ignore_conflicts=True)


def insert_region(pandas_obj):

    stack = []

    for index, row in pandas_obj.iterrows():

        city_code = int(row['АВС/ DEF'])
        region = row.Регион

        dict_obj = {
            'city_code': city_code,
            'region': region
        }

        if not (dict_obj in stack):
            stack.append({
                'city_code': city_code,
                'region': region
            })

    bulk_list = []

    for value in stack:

        city_code = value['city_code']
        geo = value['region']

        bulk_list.append(
            Region(
                city_code=city_code,
                geo=geo
            )
        )

    stack = []

    Region.objects.bulk_create(bulk_list)

    bulk_list = []


class Command(BaseCommand):

    def handle(self, *args, **options):

        csv_names = create_csv_helper()

        for csv_name in csv_names:

            pandas_obj = pandas.read_csv(
                csv_name,
                sep=';',
                usecols=['АВС/ DEF', 'От', 'До', 'Оператор', 'Регион']
            )

            insert_region(pandas_obj)
            insert_operator(pandas_obj)
            insert_phone_number(pandas_obj)


'''

CSV - file on site could be readen by pandas, but now get SSL error,
in version bellow where is SSL error.

version for reading by pandas:

https://github.com/romashovdmitry/test_case_django/blob/c9bfde38a4c859a39803f98e1d29c41270ea4a4b/test_case/management/commands/update_csv.py#L177-L209

'''
