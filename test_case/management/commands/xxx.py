# Django packages
from django.core.management import BaseCommand

from test_case.transactions import SQLTransactions


class Command(BaseCommand):

    def handle(self, *args, **options):

        x = SQLTransactions(
            city_code=999,
            number=2370953
        ).search_data()

        print(x)
