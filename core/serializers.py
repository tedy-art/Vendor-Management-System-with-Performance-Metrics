from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from datetime import datetime, timedelta

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.vendor = Vendor.objects.create(name="Vendor1", contact_details="Contact1", address="Address1", vendor_code="V1")
        self.purchase_order = PurchaseOrder.objects.create(po_number="PO1", vendor=self.vendor, order_date=datetime.now(), delivery_date=datetime.now() + timedelta(days=5), items={}, quantity=10, status='pending', issue_date=datetime.now())

    def test_vendor_list(self):
        response = self.client.get('/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        data = {
            'name': 'New Vendor',
            'contact_details': 'New Contact',
            'address': 'New Address',
            'vendor_code': 'NV'
        }
        response = self.client.post('/vendors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vendor_retrieve(self):
        response = self.client.get(f'/vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_update(self):
        data = {
            'name': 'Updated Vendor Name'
        }
        response = self.client.put(f'/vendors/{self.vendor.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_delete(self):
        response = self.client.delete(f'/vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Add more test cases for vendor endpoints (retrieve, update, delete)

    def test_purchase_order_list(self):
        response = self.client.get('/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add test cases for other purchase order endpoints (create, retrieve, update, delete, acknowledge)

    def test_historical_performance_list(self):
        response = self.client.get('/historical_performances/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add test cases for other historical performance endpoints (create, retrieve, update, delete)

    def test_authentication_required(self):
        self.client.logout()
        response = self.client.get('/vendors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_input_validation(self):
        # Test invalid data for creating a vendor
        data = {
            'name': '',  # Missing required field
            'contact_details': 'New Contact',
            'address': 'New Address',
            'vendor_code': 'NV'
        }
        response = self.client.post('/vendors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_error_handling(self):
        # Test retrieving a non-existent resource
        response = self.client.get('/vendors/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test deleting a non-existent resource
        response = self.client.delete('/vendors/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test updating a non-existent resource
        data = {'name': 'Updated Vendor Name'}
        response = self.client.put('/vendors/9999/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test acknowledging a non-existent purchase order
        response = self.client.post('/purchase_orders/9999/acknowledge/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test creating a duplicate vendor code
        data = {
            'name': 'Duplicate Vendor',
            'contact_details': 'Contact',
            'address': 'Address',
            'vendor_code': self.vendor.vendor_code  # Use existing vendor code
        }
        response = self.client.post('/vendors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
