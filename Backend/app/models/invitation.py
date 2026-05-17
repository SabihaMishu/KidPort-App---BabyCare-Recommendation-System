import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Invitation(models.Model):
    ROLE_CHOICES = [
        ('NANNY', 'Nanny'),
        ('DAYCARE', 'Daycare'),
        ('DOCTOR', 'Doctor'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('EXPIRED', 'Expired'),
    ]

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_invitations',
        limit_choices_to={'role': 'PARENT'}
    )
    role_offered = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Set default expiry to 7 days
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        if self.status == 'EXPIRED':
            return True
        if timezone.now() > self.expires_at:
            self.status = 'EXPIRED'
            self.save()
            return True
        return False

    def __str__(self):
        return f"Invite by {self.invited_by.full_name} for {self.role_offered} (Status: {self.status})"
