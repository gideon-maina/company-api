from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .factories import CompanyFactory, UserFactory
from .models import Company


class TestCompanyViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.password = 'password'
        self.user.set_password(self.password)
        self.user.save()
        self.client = APIClient()
        self.client.login(username=self.user.username, password=self.password)
        self.list_url = reverse('company-list')

    def get_detail_url(self, company_id):
        return reverse('company-detail', kwargs={'pk': company_id})

    def test_get_list(self):
        """GET the list page of Companies."""
        companies = [CompanyFactory() for i in range(12)]
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_companies_ids = [c.id for c in companies]
        actual_companies_ids = [c.get('id') for c in response.data]
        self.assertEqual(expected_companies_ids, actual_companies_ids)

    def test_get_detail(self):
        """GET a detail page for a Company."""
        company = CompanyFactory()
        response = self.client.get(self.get_detail_url(company.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], company.name)

    def test_create_company_via_post(self):
        """POST to create a Company."""
        data = {
            'name': 'gkmelsa',
            'description': 'Good company',
            'street_line_1': 'Trent Drive',
            'city': 'Nairobi',
            'state': 'NBO',
            'zipcode': '02100',
        }
        self.assertEqual(Company.objects.count(), 0)
        r = self.client.post(self.list_url, data=data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        # Get the just created company
        company = Company.objects.first()
        for field in data.keys():
            self.assertEqual(getattr(company, field), data[field])

    def test_put_company(self):
        """PUT to update a Company."""
        company = CompanyFactory()
        data = {
            'name': 'gkmelsa',
            'description': 'Good company',
            'street_line_1': 'Trent Drive',
            'city': 'Nairobi',
            'state': 'NBO',
            'zipcode': '02100',
        }
        r = self.client.put(self.get_detail_url(company.id), data=data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        # Get the refreshed PUTTED company
        company.refresh_from_db()
        for field in data.keys():
            self.assertEqual(getattr(company, field), data[field])

    def test_patch_company(self):
        """PATCH to update a Company."""
        company = CompanyFactory()
        data = {'name': 'gkmelsa'}
        r = self.client.patch(self.get_detail_url(company.id), data=data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Refresh the company
        company.refresh_from_db()
        self.assertEqual(company.name, data['name'])

    def test_delete_compant(self):
        """DELETEing is not implemented."""
        company = CompanyFactory()
        r = self.client.delete(self.get_detail_url(company.id))
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthenticated_users_cant_transact(self):
        """Unauthenticated users may not use the API."""
        self.client.logout()
        company = CompanyFactory()

        with self.subTest('GET list page'):
            r = self.client.get(self.list_url)
            self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        with self.subTest('GET detail page'):
            response = self.client.get(self.get_detail_url(company.id))
            self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        with self.subTest('POST'):
            data = {
                'name': 'gkmelsa',
                'description': 'Good company',
                'street_line_1': 'Trent Drive',
                'city': 'Nairobi',
                'state': 'NBO',
                'zipcode': '02100',
            }
            r = self.client.put(self.list_url, data=data)
            self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest('DELETE'):
            r = self.client.delete(self.get_detail_url(company.id))
            self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
            # The company was not deleted
            self.assertTrue(Company.objects.filter(id=company.id).exists())
