from django.db import models
from django.conf import settings  # ✅ TAMBAHAN LAB 9

STATUS_CHOICES = [
    ('DRAFT', 'Draft'),             # ✅ TAMBAHAN LAB 9
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]

class Report(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    reporter = models.ForeignKey(   # ✅ TAMBAHAN LAB 9
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ TAMBAHAN LAB 9

    def __str__(self):
        return self.title