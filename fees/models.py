from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    COURSE_CHOICES = [
        ('Mahad_e_Alim', 'Mahad e Alim'),
        ('course2', 'Course 2'),
        ('course3', 'Course 3'),
    ]

    BRANCH_CHOICES = [
        ('Khajabagh', 'Khajabagh'),
        ('Akberbagh', 'Akberbagh'),
        ('branch3', 'Branch 3'),
    ]

    CLASS_CHOICES = [
        ('Duwwam', 'Duwwam'),
        ('Awwal', 'Awwal'),
        ('Suwwaam', 'Suwwaam'),
        # Add other class choices
    ]

    course = models.CharField(max_length=20, choices=COURSE_CHOICES, null=True, blank=True)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES, null=True, blank=True)
    class_darja = models.CharField(max_length=20, choices=CLASS_CHOICES, null=True, blank=True)

    admission_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    monthly_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def get_total_fees(self):
        # Example calculation: Assuming total fees is calculated annually
        return self.monthly_fees * 12

    def __str__(self):
        return self.name

class Payment(models.Model):
    RECEIPT_TYPE_CHOICES = [
        ('Library Fee', 'Library Fee'),
        ('Hostel Fee', 'Hostel Fee'),
        ('Academic Fee', 'Academic Fee'),
        ('Mess Fee', 'Mess Fee'),
        ('Admission Fee', 'Admission Fee'),
        ('Examination Fee', 'Examination Fee'),
        ('Stationary Fee', 'Stationary Fee'),
        ('Other', 'Other'),
    ]

    receipt_no = models.CharField(max_length=100)
    student = models.ForeignKey(Student, to_field='admission_number', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receipt_type = models.CharField(max_length=100, choices=RECEIPT_TYPE_CHOICES)
    name = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)  # Increased length

    def __str__(self):
        return self.receipt_no
