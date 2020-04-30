from rest_framework.serializers import ModelSerializer

from .models import Company


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'description', 'website', 'street_line_1',
            'street_line_2', 'city', 'state', 'zipcode'
        ]
