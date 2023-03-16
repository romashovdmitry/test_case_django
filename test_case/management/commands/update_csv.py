# Django packages
from django.core.management import BaseCommand

# custom Django classes
from test_case.models import CSV

# libs for download CSV
from bs4 import BeautifulSoup
import requests
import urllib3
import re
import pandas
import os


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

    # delete all CSV from local and DB
    os_list = os.listdir(os.getcwd())
    for os_file in os_list:
        if '.csv' in os_file:
            os.remove(os_file)
    CSV.objects.all().delete()

    # download CSV
    download_csv_helper()

    # get names of downloaded CSV
    os_list = os.listdir(os.getcwd())
    for os_file in os_list:
        if '.csv' in os_file:
            csv_names.appen(os_file)
    return csv_names


class Command(BaseCommand):

    def handle(self, *args, **options):

        csv_names = create_csv_helper()

        for csv_name in csv_names:

            bulk_list = []

            dp = pandas.read_csv(
                csv_name,
                sep=';',
                usecols=['АВС/ DEF', 'От', 'До', 'Оператор', 'Регион']
            )

            step = 5000

            for index, row in dp.iterrows():
                if index < (step-1):
                    bulk_list.append(
                        CSV(city_code=row['АВС/ DEF'],
                            start=row.От,
                            finish=row.До,
                            operator=row.Оператор,
                            geo=row.Регион
                            )
                    )
                else:
                    step += 5000
                    CSV.objects.bulk_create(bulk_list)
                    bulk_list = []
            if bulk_list != []:
                CSV.objects.bulk_create(bulk_list)
