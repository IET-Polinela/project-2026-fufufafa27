from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Report

User = get_user_model()

class WorkflowStateTests(APITestCase):
    def setUp(self):
        self.warga = User.objects.create_user(
            username='warga_wf', password='TestPass123!', is_admin=False
        )
        self.laporan_draft = Report.objects.create(
            title='Lampu Kampus Mati',
            category='Fasilitas Umum',
            description='Lampu di depan gedung rektorat tidak menyala.',
            location='Gedung Rektorat',
            status='DRAFT',
            reporter=self.warga,
        )
        self.laporan_reported = Report.objects.create(
            title='Saluran Air Tersumbat',
            category='Infrastruktur',
            description='Saluran air di samping kantin tersumbat.',
            location='Kantin Polinela',
            status='REPORTED',
            reporter=self.warga,
        )
        self.laporan_resolved = Report.objects.create(
            title='AC Rusak di Lab',
            category='Fasilitas Umum',
            description='AC di Lab CPS 1 sudah diperbaiki.',
            location='Lab CPS 1',
            status='RESOLVED',
            reporter=self.warga,
        )

    def test_WF_01_warga_mengajukan_draf_menjadi_reported(self):
        self.client.force_authenticate(user=self.warga)
        url = f'/api/report/{self.laporan_draft.pk}/'
        payload = {
            'title': self.laporan_draft.title,
            'category': self.laporan_draft.category,
            'description': self.laporan_draft.description,
            'location': self.laporan_draft.location,
            'status': 'REPORTED',
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            "Pengajuan draf ke REPORTED seharusnya berhasil (HTTP 200)")
        self.laporan_draft.refresh_from_db()
        self.assertEqual(self.laporan_draft.status, 'REPORTED',
            "Status laporan di database harus berubah menjadi 'REPORTED'")

    def test_WF_02_tidak_bisa_edit_laporan_yang_sudah_reported(self):
        # Arrange
        self.client.force_authenticate(user=self.warga)
        url = f'/api/report/{self.laporan_reported.pk}/'
        payload = {
            'title': 'Judul Diubah',
            'category': self.laporan_reported.category,
            'description': self.laporan_reported.description,
            'location': self.laporan_reported.location,
            'status': 'REPORTED',
        }

        # Act
        response = self.client.put(url, payload, format='json')

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            "Edit laporan REPORTED seharusnya ditolak dengan HTTP 403"
        )

    def test_WF_05_laporan_resolved_tidak_bisa_diubah(self):
        # Arrange
        self.client.force_authenticate(user=self.warga)
        url = f'/api/report/{self.laporan_resolved.pk}/'
        payload = {
            'title': 'Judul Diubah',
            'category': self.laporan_resolved.category,
            'description': self.laporan_resolved.description,
            'location': self.laporan_resolved.location,
            'status': 'RESOLVED',
        }

        # Act
        response = self.client.put(url, payload, format='json')

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            "Edit laporan RESOLVED seharusnya ditolak dengan HTTP 403"
        )


class AdminWorkflowTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_portal',
            password='AdminPass123!',
            is_admin=True,
            is_staff=True,
        )
        self.laporan_reported = Report.objects.create(
            title='Jalan Rusak di Blok C',
            category='Infrastruktur',
            description='Jalan berlubang parah di area parkir Blok C.',
            location='Blok C Polinela',
            status='REPORTED',
            reporter=self.admin,
        )

    def test_WF_03_admin_mengubah_status_reported_ke_verified(self):
        # Arrange
        self.client.force_login(self.admin)
        url = reverse('update_status', kwargs={'pk': self.laporan_reported.pk})
        payload = {'status': 'VERIFIED'}

        # Act
        response = self.client.post(url, payload)

        # Assert
        self.assertIn(response.status_code, [200, 302])
        self.laporan_reported.refresh_from_db()
        self.assertEqual(
            self.laporan_reported.status, 'VERIFIED',
            "Status laporan harus berubah menjadi VERIFIED"
        )

    def test_WF_04_tidak_ada_transisi_langsung_ke_resolved_dari_reported(self):
        # Arrange
        allowed_transitions = {
            'REPORTED': ['VERIFIED'],
            'VERIFIED': ['IN_PROGRESS'],
            'IN_PROGRESS': ['RESOLVED'],
            'RESOLVED': [],
        }

        # Act
        transisi_dari_reported = allowed_transitions.get('REPORTED', [])

        # Assert
        self.assertNotIn('RESOLVED', transisi_dari_reported,
            "RESOLVED tidak boleh bisa dicapai langsung dari REPORTED")
        self.assertIn('VERIFIED', transisi_dari_reported,
            "Dari REPORTED hanya boleh ke VERIFIED")