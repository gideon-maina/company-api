from django.test import TestCase

from .serializers import CompanySerializer
from .factories import CompanyFactory


class TestCompanySerializer(TestCase):
    def test_model_fields(self):
        """Serializer data matches the Company object for each field."""
        company = CompanyFactory()
        field_names = [
            'id', 'name', 'description', 'website', 'street_line_1',
            'street_line_2', 'city', 'state', 'zipcode'
        ]
        serializer = CompanySerializer(company)

        for field_name in field_names:
            self.assertEqual(serializer.data[field_name],
                             getattr(company, field_name))
