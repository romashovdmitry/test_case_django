# import models
from test_case.models import Region, PhoneNumber

# impoer serializers
from test_case.api.serializers import AnswerSerializer

# import standart DRF packages
from rest_framework.views import APIView, Response
from rest_framework import status

# import SQL transactions by cursor
from test_case.transactions import SQLTransactions

# import Python packages
import re

errors = {

    'Wrong number': 'There is no this number in base',

    'Wrong code': 'Wrong code of city',

    "Wrong format": "Please use format XXX YYYYYYY where XXX is code of "
                    "city and YYYYYYY is number of abonent ",

    "Wrong key": "Use key 'phone_number' for requests",

    "How to find number": "Use endpoint: /api/v1/csv and JSON with key 'phone_number'"

}


class API_View(APIView):

    def get(self, request):

        if request.data:

            if 'phone_number' in request.data:

                phone_number = str(request.data['phone_number'])

                if len(phone_number) == 10 \
                        and re.match(r'^[ 0-9]+$', phone_number):

                    city_code = phone_number[:3]
                    phone_number = int(phone_number[3:])

                    if Region.objects.filter(city_code=city_code).exists():

                        db_return = SQLTransactions(
                            city_code=city_code,
                            number=phone_number
                        ).search_data()

                        if db_return is not None:

                            number_db_obj = PhoneNumber.objects.get(
                                id=db_return['id']
                            )
                            answer = AnswerSerializer(number_db_obj).data
                            return Response(
                                answer
                            )

                        # Responses for eroor cases

                        content = errors['Wrong number']

                    else:
                        content = errors['Wrong code']

                else:
                    content = errors['Wrong format']

            else:
                content = errors['Wrong key']
        else:
            content = errors['How to find number']

        return Response(
            content,
            status=status.HTTP_404_NOT_FOUND
        )
