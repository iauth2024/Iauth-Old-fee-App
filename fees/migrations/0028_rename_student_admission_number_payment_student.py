# Generated by Django 5.0.6 on 2024-08-28 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0027_remove_payment_student_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='student_admission_number',
            new_name='student',
        ),
    ]
