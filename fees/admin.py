from django.contrib import admin
from .models import Student, Payment
import logging

logger = logging.getLogger(__name__)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'name', 'phone', 'course', 'branch', 'monthly_fees']
    search_fields = ['admission_number', 'name', 'phone']

admin.site.register(Student, StudentAdmin)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_no',  'amount', 'date', 'created_by', 'receipt_type', 'name', 'payment_method', 'organization', 'year')
    search_fields = [
          # Use '__' to lookup fields in related models
        'amount',
        'date',
        'created_by__username',  # Assuming created_by is a User object
        'receipt_type',
        'name',
        'payment_method',
        'organization',
        'year',
        'receipt_no',
    ]
    def get_student_name(self, obj):
        student_name = obj.student.name if obj.student else obj.name
        logger.info(f"Student Name: {student_name}")
        return student_name
    get_student_name.short_description = 'Student Name'

    def get_student_admission_number(self, obj):
        admission_number = obj.student.admission_number if obj.student else 'N/A'
        logger.info(f"Student Admission Number: {admission_number}")
        return admission_number
    get_student_admission_number.short_description = 'Admission Number'
