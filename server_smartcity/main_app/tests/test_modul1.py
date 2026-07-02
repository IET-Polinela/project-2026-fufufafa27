from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Report

User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.warga = User.objects.create_user(
            username='warga_test',
            password='Password123!',
            is_admin=False,
        )
        self.admin = User.objects.create_user(
            username='admin_test',
            password='AdminPass123!',
            is_admin=True,
            is_staff=True,
        )

    def test_AUTH_01_login_warga_dengan_kredensial_valid(self):
        url = reverse('token_obtain_pair')
        payload = {
            'username': 'warga_test',
            'password': 'Password123!',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            "Login dengan kredensial valid seharusnya mengembalikan HTTP 200")
        self.assertIn('access', response.data,
            "Respons login harus mengandung field 'access' (JWT Access Token)")
        self.assertIn('refresh', response.data,
            "Respons login harus mengandung field 'refresh' (JWT Refresh Token)")

    def test_AUTH_02_login_warga_dengan_password_salah(self):
        url = reverse('token_obtain_pair')
        payload = {
            'username': 'warga_test',
            'password': 'passwordSALAH',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
            "Login dengan password salah seharusnya mengembalikan HTTP 401")
        self.assertNotIn('access', response.data,
            "Tidak boleh ada token yang dikeluarkan untuk kredensial invalid")

    def test_AUTH_03_warga_tidak_bisa_akses_halaman_admin(self):
        # Arrange: login sebagai warga biasa (is_staff=False)
        self.client.force_login(self.warga)

        # Act: akses halaman dashboard admin
        url = reverse('dashboard')
        response = self.client.get(url)

        # Assert: harus di-redirect (302) karena bukan staff
        self.assertIn(response.status_code, [302, 403])