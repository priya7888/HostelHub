from django.db import models
from django.contrib.auth.models import User
import uuid

class OutingRequest(models.Model):
    STATUS = [
        ('pending',           'Pending Parent Approval'),
        ('parent_approved',   'Parent Approved'),
        ('parent_rejected',   'Parent Rejected'),
        ('warden_approved',   'Warden Approved'),
        ('warden_rejected',   'Warden Rejected'),
        ('checked_out',       'Checked Out'),
        ('returned',          'Returned'),
    ]

    student          = models.ForeignKey(User, on_delete=models.CASCADE,
                         related_name='outing_requests')
    reason           = models.TextField()
    destination      = models.CharField(max_length=200)
    out_date         = models.DateField()
    out_time         = models.TimeField()
    return_date      = models.DateField()
    return_time      = models.TimeField()
    status           = models.CharField(max_length=30,
                         choices=STATUS, default='pending')

    # Parent
    parent_token     = models.UUIDField(default=uuid.uuid4, unique=True)
    parent_approved_at = models.DateTimeField(null=True, blank=True)
    parent_remarks   = models.TextField(blank=True)

    # Warden
    warden           = models.ForeignKey(User, on_delete=models.SET_NULL,
                         null=True, blank=True, related_name='outing_approvals')
    warden_approved_at = models.DateTimeField(null=True, blank=True)
    warden_remarks   = models.TextField(blank=True)

    # QR
    qr_token         = models.UUIDField(default=uuid.uuid4, unique=True)
    qr_generated     = models.BooleanField(default=False)

    # Timestamps
    created_at       = models.DateTimeField(auto_now_add=True)
    checked_out_at   = models.DateTimeField(null=True, blank=True)
    returned_at      = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.destination} - {self.status}"