from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Report

User = get_user_model()

class CRUDAndValidationTests(APITestCase):
    def setUp(self):
        self.warga = User.objects.create_user(
            username='warga_crud', password='TestPass123!', is_admin=False
        )
        self.client.force_authenticate(user=self.warga)

    def test_FT_01_buat_laporan_dengan_data_lengkap(self):
        # Arrange
        url = reverse('report-list')
        payload = {
            'title': 'Jalan Berlubang di Depan Kantor',
            'category': 'Infrastruktur',
            'description': 'Ada lubang besar yang berbahaya.',
            'location': 'Jl. Sudirman No. 1',
        }

        # Act
        response = self.client.post(url, payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Pembuatan laporan dengan data lengkap harus berhasil (HTTP 201)")
        self.assertEqual(
            Report.objects.filter(title='Jalan Berlubang di Depan Kantor').count(), 1,
            "Laporan harus tersimpan di database")
        self.assertEqual(response.data['reporter'], 'Warga Anonim',
            "Field reporter harus disamarkan")

    def test_FT_02_ditolak_jika_judul_kosong(self):
        # Arrange
        url = reverse('report-list')
        payload = {
            'category': 'Infrastruktur',
            'description': 'Deskripsi ada tapi judul tidak ada.',
            'location': 'Jl. Sudirman',
        }

        # Act
        response = self.client.post(url, payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Request tanpa title harus ditolak dengan HTTP 400")
        self.assertIn('title', response.data)

    def test_FT_03_ditolak_jika_deskripsi_kosong(self):
        # Arrange
        url = reverse('report-list')
        payload = {
            'title': 'Laporan Tanpa Deskripsi',
            'category': 'Infrastruktur',
            'location': 'Jl. Sudirman',
        }

        # Act
        response = self.client.post(url, payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Request tanpa description harus ditolak dengan HTTP 400")
        self.assertIn('description', response.data)

    def test_FT_04_xss_script_disimpan_sebagai_string_literal(self):
        url = reverse('report-list')
        kode_xss = '<script>alert("xss")</script>'
        payload = {
            'title': 'Laporan XSS Test',
            'category': 'Keamanan',
            'description': kode_xss,
            'location': 'Lab Keamanan Siber',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Data dengan karakter HTML harus tetap diterima oleh API")
        laporan = Report.objects.get(title='Laporan XSS Test')
        self.assertIn('script', laporan.description.lower(),
            "Kode XSS harus tersimpan sebagai string literal di database")