from rest_framework import serializers
from test_case.models import Region, Operator, PhoneNumber


# https://stackoverflow.com/questions/51323922/how-can-i-have-two-models-in-one-serializer-in-django

class GetPKData(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            'geo',
        )


class AnswerSerializer(serializers.ModelSerializer):

    # to get data from an other table, that include FK of table PhoneNumber
    region = GetPKData()

    class Meta:
        model = PhoneNumber
        fields = (
            'operator',
            'region'
        )
