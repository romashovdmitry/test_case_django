from rest_framework.generics import RetrieveAPIView
from django.shortcuts import render
from test_case.models import CSV
from test_case.api.serializers import CSVSerializer
from django.forms import model_to_dict

from django.http import Http404
from rest_framework.views import APIView, Response
from rest_framework import status


class CSVAPIView(APIView):

    def get(self, request):
        
        if request.data:

            if 'phone_number' in request.data:

                phone_number = str(request.data['phone_number'])
                city_code = phone_number[:3]
                phone_number = int(phone_number[3:])
        
                if CSV.objects.filter(city_code=city_code).exists():
                    csv_rows = CSV.objects.filter(city_code=city_code).all()
                    for row in csv_rows:
                        if row.start == phone_number or\
                            row.finish == phone_number or\
                                row.start < phone_number < row.finish:
                            answer = CSVSerializer(row).data
                            return Response(
                                answer
                            )
                    content = {
                        'Wrong data': 'There is no this number in base'
                    }
                    return Response(
                        content,
                        status=status.HTTP_404_NOT_FOUND
                    )
                else:
                    content = {
                        'Wrong data': 'Wrong code of city'
                    }
                    return Response(
                        content,
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                content = {
                    "Wrong key": "Use key 'phone_number'"
                }
                return Response(
                        content,
                        status=status.HTTP_404_NOT_FOUND
                    )
        else:
            content = {
                "How to find number": "Use endpoint: /api/v1/csv and JSON with key 'phone_number'"
            }
            return Response(
                    content,
                    status=status.HTTP_404_NOT_FOUND
                )