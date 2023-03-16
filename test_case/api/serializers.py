from rest_framework import serializers
from test_case.models import CSV


class CSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSV
        fields = (
            'operator',
            'geo'
        )
