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


def insert_phone_number(pandas_obj):

    bulk_list = []

    step = 5000

    for index, row in pandas_obj.iterrows():
        if index < (step-1):
            region_pk = Region.objects.filter(geo=row.Регион).filter(
                city_code=row['АВС/ DEF']).first()
            operator = Operator.objects.get(operator=row.Оператор)
            bulk_list.append(
                PhoneNumber(
                    start=row.От,
                    finish=row.До,
                    region_pk=region_pk,
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

        SQLTransactions().delete_all_data()

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

                csv_file = link.get('href')
                pandas_obj = pandas.read_csv(
                    csv_file,
                    sep=';',
                    usecols=['АВС/ DEF', 'От', 'До', 'Оператор', 'Регион']
                )

                insert_region(pandas_obj)
                insert_operator(pandas_obj)
                insert_phone_number(pandas_obj)
