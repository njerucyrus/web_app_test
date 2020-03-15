from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from django.db.models.signals import post_save

from scolarship import settings


class ScholarshipApplication(models.Model):
    ACADEMIC_LEVEL_CHOICES = (
        ('primary', 'primary'),
        ('high school', 'high school'),
        ('diploma', 'diploma'),
        ('undergraduate', 'undergraduate'),
        ('masters', 'masters'),
        ('PhD', 'PhD'),
    )

    APPLICATION_STATUS = (
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
        ('selected', 'selected')
    )
    student_name = models.CharField(max_length=64, null=False, blank=False)
    address = models.CharField(max_length=140, null=False, blank=False)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    birth_certificate = models.FileField(upload_to='attachments/certs/')
    id_no = models.FileField(upload_to='attachments/ids/')
    school_name = models.CharField(max_length=128, null=False, blank=False)
    school_address = models.CharField(max_length=140, null=False, blank=False)
    academic_level = models.CharField(max_length=32, choices=ACADEMIC_LEVEL_CHOICES,
                                      default=ACADEMIC_LEVEL_CHOICES[0][0])
    recommendation_reason = models.TextField(max_length=256, )
    recommendation_letter = models.FileField(upload_to='attachments/letters/')
    year = models.PositiveIntegerField(default=2020)
    application_status = models.CharField(max_length=32, choices=APPLICATION_STATUS, default=APPLICATION_STATUS[0][0])
    date_applied = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('application_status', '-date_applied')

    def __str__(self):
        return "{0}-Application#{1}".format(self.student_name, self.pk)


def on_application_modified(sender, instance, **kwargs):
    """Send email notification to notify the applicant on the status of the application"""
    message = ''
    if instance.application_status == 'approved':
        message = f"Dear {instance.student_name} We are pleased to inform you that your scholership application to {instance.school_name} has been approved."

    if instance.application_status == 'rejected':
        message = f"Dear {instance.student_name} this is to inform you that your application was rejected since it did not pass the expected criteria"

    send_mail('Application Status Notification', message, settings.DEFAULT_FROM_EMAIL, [instance.email],
              fail_silently=False)


post_save.connect(on_application_modified, sender=ScholarshipApplication)
