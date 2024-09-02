from decimal import Decimal
import io
from multiprocessing import context
from venv import logger
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Sum
from fees.forms import  PaymentForm
from .models import Student, Payment
from django.urls import reverse
from django.db.models import F
import csv
from django.contrib.auth.models import User


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
#######################################################################################################################

def receipt_number_input(request):
    if request.method == 'POST':
        receipt_no = request.POST.get('receipt_no')
        if receipt_no:
            return redirect(reverse('print_receipt', kwargs={'receipt_no': receipt_no}))
    return render(request, 'receipt_number_input.html')

def print_receipt(request, receipt_no):
    # Retrieve the receipt using the provided receipt number
    receipt = get_object_or_404(Payment, receipt_no=receipt_no)
    
    # Pass the receipt to the template
    context = {
        'receipt': receipt,
    }
    
    return render(request, 'print_receipt.html', context)



######################################################################################################################

from .models import Payment, Student

from django.shortcuts import render
from .models import Payment, Student
from django.shortcuts import render
from .models import Student, Payment

from django.shortcuts import render
from django.db.models import Sum
from .models import Student, Payment

from django.shortcuts import render
from .models import Payment  # Ensure you import your models
from django.http import JsonResponse
from .models import Student

def fetch_student_details(request):
    admission_number = request.GET.get('admission_number', None)
    if admission_number:
        try:
            student = Student.objects.get(admission_number=admission_number)
            data = {
                'name': student.name,
                'course': student.course,
                'class': student.class_darja,  # Adjust the field names as per your model
            }
            return JsonResponse(data)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def student_receipt_list(request):
    # Define the receipt types you're dealing with
    receipt_types = ['Library Fee', 'Hostel Fee', 'Academic Fee', 'Mess Fee', 'Admission Fee', 'Examination Fee', 'Stationary Fee']

    # Define the allowed thresholds for each receipt type
    allowed_receipt_types = {
        'Library Fee': 3600,
        'Hostel Fee': 12000,
        'Academic Fee': 12000,
        'Mess Fee': 48000,
        'Admission Fee': 2000,
        'Examination Fee': 400,
        'Stationary Fee': 4000,
    }

    # Get the selected year from the GET parameters
    selected_year = request.GET.get('year', None)

    # Fetch distinct years from the Payment model
    years = Payment.objects.values_list('year', flat=True).distinct()

    # Filter payments based on the selected year
    if selected_year:
        payments = Payment.objects.filter(year=selected_year)
    else:
        payments = Payment.objects.all()

    # Prepare student data
    student_data = {}
    for payment in payments:
        student_name = payment.name
        receipt_type = payment.receipt_type
        amount = payment.amount
        
        # Skip fee types not included in receipt_types
        if receipt_type not in receipt_types:
            continue
        
        if student_name not in student_data:
            student_data[student_name] = {rt: 0 for rt in receipt_types}
        
        student_data[student_name][receipt_type] += amount

    context = {
        'receipt_types': receipt_types,
        'allowed_receipt_types': allowed_receipt_types,
        'student_data': student_data,
        'years': years,
        'selected_year': selected_year,
    }
    
    return render(request, 'student_receipt_list.html', context)




########################################################################################################################
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to homepage after login
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    
from django.shortcuts import redirect

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to login page after logout
    else:
        # Handle GET requests by redirecting to the login page
        return redirect('login')

@login_required
def homepage(request):
    return render(request, 'homepage.html')


##########################################################################################################################

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PaymentForm
from .models import Payment, Student
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import PaymentForm
from .models import Student, Payment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError  # Add this import statement
from django.contrib.admin.views.decorators import staff_member_required

@login_required
@staff_member_required  # Ensures only staff members can access the view
def download_payments(request):
    payments = Payment.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Receipt No', 'Student Admission No', 'Student Name', 'Amount', 'Date', 'Created By'])

    for payment in payments:
        # Check if payment.student is not None
        if payment.student:
            admission_number = payment.student.admission_number
            student_name = payment.student.name
        else:
            admission_number = 'N/A'
            student_name = 'N/A'

        writer.writerow([
            payment.receipt_no,
            admission_number,
            student_name,
            payment.amount,
            payment.date,
            payment.created_by.username if payment.created_by else ''  # Use username if available, else empty string
        ])

    return response


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import PaymentForm, OtherPaymentForm  # Assuming you have these forms
from .models import Payment, Student, User
import datetime

def generate_receipt_number(receipt_date):
    if datetime.date(2022, 4, 1) <= receipt_date <= datetime.date(2023, 3, 31):
        prefix = '22-'
    elif datetime.date(2023, 4, 1) <= receipt_date <= datetime.date(2024, 3, 31):
        prefix = '23-'
    else:
        return None, "This software does not support creating receipts after 01/04/2024."
    
    last_payment = Payment.objects.filter(receipt_no__startswith=prefix).order_by('receipt_no').last()
    if last_payment:
        last_number = int(last_payment.receipt_no.split('-')[1])
    else:
        last_number = 0
    
    new_number = last_number + 1
    return f"{prefix}{new_number:05d}", None

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .forms import PaymentForm, OtherPaymentForm
from .models import Payment, Student
from django.contrib.auth.models import User

def generate_receipt_number(receipt_date):
    # Implement your receipt number generation logic
    # Example:
    return "RECEIPT123456", None
def get_student_details(request):
    admission_number = request.GET.get('admission_number')
    try:
        student = Student.objects.get(admission_number=admission_number)
        response_data = {
            'success': True,
            'student': {
                'admission_number': student.admission_number,
                'name': student.name,
                'phone': student.phone,
                'address': student.address,  # Assuming the Student model has these fields
                'fees': student.monthly_fees,  # Or however you are storing fees
                'total_amount': student.get_total_amount()  # If you have a method to calculate total amount
            }
        }
    except Student.DoesNotExist:
        response_data = {'success': False}
def make_payment(request):
    current_tab = 'fee'  # default tab
    form = None  # Ensure form is always defined
    other_form = None  # Ensure other_form is always defined

    if request.method == 'POST':
        if 'fee_payment' in request.POST:
            form = PaymentForm(request.POST)
            current_tab = 'fee'
        elif 'other_payment' in request.POST:
            form = OtherPaymentForm(request.POST)
            current_tab = 'other'

        if form and form.is_valid():  # Check if form is defined and valid
            receipt_date = timezone.now().date()
            receipt_number, error_message = generate_receipt_number(receipt_date)
            if error_message:
                messages.error(request, error_message)
                return render(request, 'make_payment.html', {'form': form, 'current_tab': current_tab})

            if current_tab == 'fee':
                admission_number = form.cleaned_data.get('admission_number')
                amount_paid = form.cleaned_data.get('amount_paid')
                receipt_type = form.cleaned_data.get('receipt_type')

                try:
                    student = Student.objects.get(admission_number=admission_number)
                except Student.DoesNotExist:
                    student = None

                created_by = User.objects.get(username=request.user.username)

                payment = Payment.objects.create(
                    student=student,
                    amount=amount_paid,
                    receipt_no=receipt_number,
                    created_by=created_by,
                    name=student.name if student else "Unknown",
                    receipt_type=receipt_type
                )

            elif current_tab == 'other':
                name = form.cleaned_data.get('name')
                phone = form.cleaned_data.get('phone')
                address = form.cleaned_data.get('address')
                amount_paid = form.cleaned_data.get('amount_paid')
                payment_method = form.cleaned_data.get('payment_method')
                receipt_type = form.cleaned_data.get('receipt_type')

                payment = Payment.objects.create(
                    student=None,  # No student associated for 'Other' payments
                    amount=amount_paid,
                    receipt_no=receipt_number,

                    created_by=User.objects.get(username=request.user.username),
                    name=name,
                    receipt_type=receipt_type,
                    address=address,
                    phone=phone,
                    payment_method=payment_method
                )

            messages.success(request, 'Payment has been recorded successfully.')
            return redirect('payment_list')

        else:
            messages.error(request, 'Form is not valid. Please correct the errors.')

    else:
        # Initialize forms if the request method is GET
        if current_tab == 'fee':
            form = PaymentForm()
        elif current_tab == 'other':
            form = OtherPaymentForm()

    return render(request, 'make_payment.html', {'form': form, 'current_tab': current_tab})
from django.shortcuts import render
from .models import Student

def make_payment(request):
    message = "This software is no longer in use. Visit the new updated software at https://iauth-accounts.onrender.com/"
    
    context = {
        'message': message
    }
    
    return render(request, 'make_payment.html', context)


from django.shortcuts import render
from .models import Student, Payment

def payment_success(request):
    admission_number = request.GET.get('admission_number')
    if not admission_number:
        return render(request, 'payment_success.html', {
            'error_message': 'Admission number is required.'
        })

    try:
        student = Student.objects.get(admission_number=admission_number)
    except Student.DoesNotExist:
        return render(request, 'payment_success.html', {
            'error_message': 'No student found with the provided admission number.'
        })

    payment_details = Payment.objects.filter(student=student).order_by('-date')

    if not payment_details:
        return render(request, 'payment_success.html', {
            'student': student,
            'error_message': 'No payments found for this student.'
        })

    return render(request, 'payment_success.html', {
        'student': student,
        'payment_details': payment_details
    })



from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from .forms import PaymentUploadForm
from .models import Payment, Student
from django.contrib.auth.models import User

import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import Payment, Student

from django.core.exceptions import ValidationError



import pandas as pd
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render

import logging

# Set up logging
logger = logging.getLogger(__name__)
@login_required
@user_passes_test(lambda u: u.is_staff)
def upload_payments(request):
    if request.method == 'POST':
        form = PaymentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # Dictionary to hold the totals for each student and receipt_type
            fee_totals = {}

            for index, row in df.iterrows():
                receipt_no = str(row.get('Receipt No', '')).strip()
                student_admission_no = str(row.get('Student Admission No', '')).strip()
                amount_str = str(row.get('Amount', '')).strip()
                date_value = row.get('Date', None)
                created_by_username = str(row.get('Created By', '')).strip()
                receipt_type = str(row.get('receipt_type', '')).strip()
                name = str(row.get('Name', '')).strip()
                payment_method = str(row.get('Payment Method', '')).strip()
                organization = str(row.get('Organization', '')).strip()
                year = str(row.get('Year', '')).strip()

                try:
                    amount = float(amount_str.replace(',', ''))
                except ValueError:
                    print(f"Invalid amount '{amount_str}' in row {index + 1}")
                    continue

                if pd.notna(date_value):
                    try:
                        date = pd.to_datetime(date_value).date()
                    except ValueError:
                        print(f"Invalid date '{date_value}' in row {index + 1}")
                        continue
                else:
                    date = None

                if student_admission_no:
                    try:
                        student = Student.objects.get(admission_number=student_admission_no)
                    except Student.DoesNotExist:
                        print(f"Student with admission number '{student_admission_no}' does not exist in row {index + 1}")
                        student = None
                else:
                    student = None

                if created_by_username:
                    try:
                        created_by = User.objects.get(username=created_by_username)
                    except User.DoesNotExist:
                        print(f"User with username '{created_by_username}' does not exist in row {index + 1}")
                        created_by = None
                else:
                    created_by = None

                try:
                    payment = Payment(
                        receipt_no=receipt_no,
                        student=student,
                        amount=amount,
                        date=date,
                        created_by=created_by,
                        receipt_type=receipt_type,
                        name=name,
                        payment_method=payment_method,
                        organization=organization,
                        year=year
                    )
                    payment.save()
                    print(f"Saved payment: {payment}")

                    # Update the fee totals for the student and receipt_type
                    if student_admission_no not in fee_totals:
                        fee_totals[student_admission_no] = {}

                    if receipt_type not in fee_totals[student_admission_no]:
                        fee_totals[student_admission_no][receipt_type] = 0

                    fee_totals[student_admission_no][receipt_type] += amount

                except ValidationError as e:
                    print(f"Validation error for row {index + 1}: {e}")
                except Exception as e:
                    print(f"Error saving payment for row {index + 1}: {e}")

            # Display or save the fee totals
            for student_admission_no, receipt_totals in fee_totals.items():
                print(f"Total fees for student {student_admission_no}:")
                for receipt_type, total in receipt_totals.items():
                    print(f"  {receipt_type}: {total}")

            return HttpResponse('Payments uploaded successfully')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = PaymentUploadForm()

    return render(request, 'upload_payments.html', {'form': form})



def calculate_total_due(student):
    # Placeholder function to calculate total due for a student
    total_fees = student.total_fees  # Assuming you have a field named 'total_fees' in your Student model
    total_paid = student.payment_set.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
    total_due = total_fees - total_paid
    return total_due



def get_student_details(request):
    if request.method == 'GET':
        admission_number = request.GET.get('admission_number')
        try:
            student = Student.objects.get(admission_number=admission_number)
            total_fees_paid = sum(payment.amount for payment in student.payment_set.all())
            total_due = student.total_fees - total_fees_paid
            months_paid = total_fees_paid / student.monthly_fees
            # Round off to 2 decimal places for monetary values
            total_fees_paid = round(total_fees_paid)
            total_due = round(total_due)
            # Round off to 1 decimal place for months_paid
            months_paid = round(months_paid, 1)
            data = {
                'name': student.name,
                'phone': student.phone,
                'course': student.course,
                'branch': student.branch,
                'monthly_fees': int(student.monthly_fees),  # Convert to integer to remove decimal places
                'total_fees': int(student.total_fees),  # Convert to integer to remove decimal places
                'total_paid': total_fees_paid,
                'total_due': total_due,
                'months_paid': months_paid
            }
            return JsonResponse({'success': True, 'student': data})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Admission number not found'}, status=404)


from django.shortcuts import render
from django.db.models import Sum
from .models import Student, Payment
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from xhtml2pdf import pisa # type: ignore
from django.template.loader import get_template
from django.db.models import Sum
from django.shortcuts import render

from django.shortcuts import render
from django.db.models import Sum
from .models import Student, Payment

def reports(request):
    # Fetch all students initially
    students = Student.objects.all()

    # Get unique choices for branch and class_darja
    branch_choices = Student.BRANCH_CHOICES
    class_choices = Student.CLASS_CHOICES
    course_choices = Student.COURSE_CHOICES  # Add this line

    # Get filter parameters from the request
    course = request.GET.get('course', '')
    branch = request.GET.get('branch', '')
    class_darja = request.GET.get('class_darja', '')
    months_paid = request.GET.get('months_paid', '')

    # Apply filters if provided
    if course:
        students = students.filter(course=course)
    if branch:
        students = students.filter(branch=branch)
    if class_darja:
        students = students.filter(class_darja=class_darja)

    # Calculate months paid for each student and filter based on the provided months_paid
    filtered_students = []
    if months_paid.isdigit():
        months_paid = int(months_paid)
        for student in students:
            total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
            paid_months = total_paid / student.monthly_fees if student.monthly_fees else 0
            if paid_months < months_paid:
                filtered_students.append(student)
    else:
        filtered_students = students

    # Calculate total fees paid and outstanding fees for each filtered student
    additional_info = []
    for student in filtered_students:
        total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
        total_due = student.total_fees - total_paid
        months_paid_count = total_paid / student.monthly_fees if student.monthly_fees != 0 else 0
        additional_info.append({
            'student': student,
            'monthly_fees': student.monthly_fees,
            'total_fees': student.total_fees,
            'total_paid': total_paid,
            'total_due': total_due,
            'months_paid': months_paid_count,
        })

    context = {
        'additional_info': additional_info,
        'branch_choices': branch_choices,
        'class_choices': class_choices,
        'course_choices': course_choices,  # Add this line
        'course': course,
        'branch': branch,
        'selected_class_darja': class_darja,
        'selected_months_paid': months_paid,
    }
    return render(request, 'reports.html', context)



def generate_pdf(request):
    # Generate the PDF
    students = Student.objects.all()
    # Get filter parameters from the request
    course = request.GET.get('course', '')
    branch = request.GET.get('branch', '')
    class_darja = request.GET.get('class_darja', '')
    months_paid = request.GET.get('months_paid', '')

    # Apply filters if provided
    if course:
        students = students.filter(course=course)
    if branch:
        students = students.filter(branch=branch)
    if class_darja:
        students = students.filter(class_darja=class_darja)
    if months_paid.isdigit():
        months_paid = int(months_paid)
        students = [student for student in students if (Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0) / student.monthly_fees >= months_paid]

    additional_info = []
    for student in students:
        total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
        total_due = student.total_fees - total_paid
        months_paid_count = total_paid / student.monthly_fees if student.monthly_fees != 0 else 0
        additional_info.append({
            'student': student,
            'monthly_fees': student.monthly_fees,
            'total_fees': student.total_fees,
            'total_paid': total_paid,
            'total_due': total_due,
            'months_paid': months_paid_count,
        })

    context = {
        'additional_info': additional_info,
    }

    template_path = 'pdf_template.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Sum
from .models import Student, Payment

def generate_excel(request):
    # Generate the Excel
    students = Student.objects.all()
    # Get filter parameters from the request
    course = request.GET.get('course', '')
    branch = request.GET.get('branch', '')
    class_darja = request.GET.get('class_darja', '')
    months_paid = request.GET.get('months_paid', '')

    # Apply filters if provided
    
    if months_paid.isdigit():
        months_paid = int(months_paid)
        students = students.annotate(total_paid=Sum('payment__amount')).filter(total_paid__gte=F('monthly_fees') * months_paid)

    # Create a new Workbook object
    wb = Workbook()

    # Create a worksheet
    ws = wb.active

    # Add headers to the worksheet
    headers = ['Admission Number', 'Name', 'Course', 'Branch', 'Class', 'Monthly Fees', 'Total Fees', 'Total Paid', 'Total Due', 'Months Paid']
    ws.append(headers)

    # Add student data to the worksheet
    for student in students:
        total_paid = student.payment_set.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
        total_due = student.total_fees - total_paid
        months_paid_count = total_paid / student.monthly_fees if student.monthly_fees != 0 else 0

        row_data = [
            student.admission_number,
            student.name,
            student.course,
            student.branch,
            student.class_darja,
            student.monthly_fees,
            student.total_fees,
            total_paid,
            total_due,
            months_paid_count
        ]
        ws.append(row_data)

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'

    # Save the workbook to the HTTP response
    wb.save(response)

    return response







from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'custom_password_reset.html'
    email_template_name = 'custom_password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'custom_password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'custom_password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'custom_password_reset_complete.html'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, FloatField
from django.db.models import ExpressionWrapper, F
from django.shortcuts import render

from collections import defaultdict  # Import defaultdict
@login_required

def summary(request):
    selected_organization = request.GET.get('organization', '')
    selected_year = request.GET.get('year', '')

    organizations = Payment.objects.values_list('organization', flat=True).distinct()
    years = Payment.objects.values_list('year', flat=True).distinct()

    payments = Payment.objects.all()
    if selected_organization:
        payments = payments.filter(organization=selected_organization)
    if selected_year:
        payments = payments.filter(year=selected_year)

    total_students = payments.count()
    total_fees = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    students_with_no_due = ...  # Calculate based on your logic
    payment_methods = list(payments.values_list('payment_method', flat=True).distinct())
    receipt_types = list(payments.values_list('receipt_type', flat=True).distinct())

    data = {}
    for receipt_type in receipt_types:
        data[receipt_type] = {}
        for method in payment_methods:
            total = payments.filter(receipt_type=receipt_type, payment_method=method).aggregate(Sum('amount'))['amount__sum'] or 0
            data[receipt_type][method] = total

    row_totals = {receipt_type: sum(data[receipt_type].values()) for receipt_type in receipt_types}
    column_totals = {method: payments.filter(payment_method=method).aggregate(Sum('amount'))['amount__sum'] or 0 for method in payment_methods}
    grand_total = sum(column_totals.values())

    context = {
        'total_students': total_students,
        'total_fees': total_fees,
        'grand_total': grand_total,
        'students_with_no_due': students_with_no_due,
        'payment_methods': payment_methods,
        'data': data,
        'row_totals': row_totals,
        'column_totals': column_totals,
        'organizations': organizations,
        'years': years,
        'selected_organization': selected_organization,
        'selected_year': selected_year,
    }
    return render(request, 'summary.html', context)
############################################################################################################################\




@login_required
def user_payments(request):
    user_payments = Payment.objects.filter(created_by=request.user).order_by('-date')

    for payment in user_payments:
        if payment.student is None:
            print(f"Payment {payment.receipt_no} has no student linked.")

    context = {
        'user_payments': user_payments,
    }
    return render(request, 'user_payments.html', context)




from django.db.models import Sum

# views.py


from django.shortcuts import render
from .models import Payment
from .forms import PaymentFilterForm

def student_payment_report(request):
    form = PaymentFilterForm(request.GET or None)
    payments = Payment.objects.all().order_by('-date')

    if form.is_valid():
        # Filter by each field if it has a value
        if form.cleaned_data['receipt_no']:
            payments = payments.filter(receipt_no__icontains=form.cleaned_data['receipt_no'])
        if form.cleaned_data['amount']:
            payments = payments.filter(amount=form.cleaned_data['amount'])
        if form.cleaned_data['date']:
            payments = payments.filter(date=form.cleaned_data['date'])
        if form.cleaned_data['created_by']:
            payments = payments.filter(created_by__icontains=form.cleaned_data['created_by'])
        if form.cleaned_data['receipt_type']:
            payments = payments.filter(receipt_type__icontains=form.cleaned_data['receipt_type'])
        if form.cleaned_data['name']:
            payments = payments.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data['payment_method']:
            payments = payments.filter(payment_method__icontains=form.cleaned_data['payment_method'])
        if form.cleaned_data['organization']:
            payments = payments.filter(organization__icontains=form.cleaned_data['organization'])
        if form.cleaned_data['year']:
            payments = payments.filter(year__icontains=form.cleaned_data['year'])

    # Prepare data for list display
    payment_data = payments.values(
        'receipt_no', 'amount', 'date', 'created_by', 'receipt_type', 'name', 'payment_method', 'organization', 'year'
    )

    return render(request, 'student_payment_report.html', {
        'form': form,
        'payment_data': payment_data
    })



    


# forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

# views.py
import pandas as pd
from .forms import UploadFileForm
from .models import Student

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from .forms import UploadFileForm
from .models import Student

@login_required
@user_passes_test(lambda u: u.is_staff)  # Ensure only admin users can access this view
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
                success_students = []
                failed_students = []
                already_exists_students = []

                for index, row in df.iterrows():
                    admission_number = row.get('Admission Number')
                    name = row.get('Name')

                    if not admission_number or not name:
                        failed_students.append({
                            'admission_number': admission_number,
                            'name': name,
                            'reason': 'Admission Number and Name are required'
                        })
                        continue

                    if Student.objects.filter(admission_number=admission_number).exists():
                        already_exists_students.append({
                            'admission_number': admission_number,
                            'name': name,
                            'reason': 'Already Exists'
                        })
                    else:
                        # Get optional fields with default values
                        phone = row.get('Phone', '')
                        course = row.get('Course', '')
                        class_darja = row.get('Class', 'Duwwam')
                        branch = row.get('Branch', '')
                        monthly_fees = row.get('Monthly Fees', 0)

                        # Create new student
                        student = Student(
                            admission_number=admission_number,
                            name=name,
                            phone=phone,
                            course=course,
                            class_darja=class_darja,
                            branch=branch,
                            monthly_fees=monthly_fees
                        )
                        student.save()
                        success_students.append(student)

                total_students_to_upload = len(df)
                already_exists_no = len(already_exists_students)
                failed_no = len(failed_students)
                success_no = total_students_to_upload - failed_no - already_exists_no
                newly_added_no = success_no

                return render(request, 'upload_result.html', {
                    'total_students_to_upload': total_students_to_upload,
                    'already_exists_no': already_exists_no,
                    'failed_no': failed_no,
                    'success_no': success_no,
                    'newly_added_no': newly_added_no,
                    'already_exists_students': already_exists_students,
                    'failed_students': failed_students,
                    'success_students': success_students,
                })

    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})
