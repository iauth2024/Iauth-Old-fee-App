from django import forms
from .models import Payment

class PaymentForm(forms.Form):
    admission_number = forms.CharField(label="Admission Number", required=True)
    name = forms.CharField(label="Name", required=True)  # Mandatory field
    amount_paid = forms.DecimalField(label="Amount Paid", required=True)
    receipt_number = forms.CharField(label="Receipt Number", required=True)
    receipt_type = forms.CharField(label="Receipt Type", required=True)  # Mandatory field
    date = forms.DateField(label="Date", required=True)
    created_by = forms.CharField(label="Created By", required=True)
    fee_type = forms.CharField(label="Fee Type", required=True)
    payment_method = forms.CharField(label="Payment Method", required=True)
    transaction_id = forms.CharField(label="Transaction ID", required=False)

class OtherPaymentForm(forms.Form):
    name_other = forms.CharField(label="Name", required=True)
    phone = forms.CharField(label="Phone", required=True)
    address = forms.CharField(label="Address", required=True)
    amount_other = forms.DecimalField(label="Amount", required=True)
    payment_method = forms.CharField(label="Payment Method", required=True)
    receipt_type_other = forms.CharField(label="Receipt Type", required=True)
    receipt_number_other = forms.CharField(label="Receipt Number", required=True)
    date_other = forms.DateField(label="Date", required=True)
    created_by_other = forms.CharField(label="Created By", required=True)

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file')

class PaymentUploadForm(forms.Form):
    excel_file = forms.FileField()
from django import forms
from .models import Payment

class PaymentFilterForm(forms.Form):
    receipt_no = forms.CharField(required=False, label='Receipt No')
    amount = forms.DecimalField(required=False, label='Amount', decimal_places=2)
    date = forms.DateField(required=False, label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    created_by = forms.CharField(required=False, label='Created By')
    receipt_type = forms.CharField(required=False, label='Receipt Type')
    name = forms.CharField(required=False, label='Name')
    payment_method = forms.CharField(required=False, label='Payment Method')
    organization = forms.CharField(required=False, label='Organization')
    year = forms.CharField(required=False, label='Year')
