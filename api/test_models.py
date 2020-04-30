from django.test import TestCase

from .models import Company
from .factories import CompanyFactory


class CompanyModelTestCase(TestCase):
    def test_str(self):
        """ Test for __str__ representation """
        company = CompanyFactory()
        self.assertEqual(str(company),
                         f"Company {company.name} in {company.city}")
