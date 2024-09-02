# Generated by Django 5.0.6 on 2024-07-09 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0017_alter_payment_receipt_type_alter_payment_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(choices=[('Khaja Bagh', 'Khaja Bagh'), ('Akber Bagh', 'Akber Bagh'), ('Ghatkesar', 'Ghatkesar'), ('Bandlaguda', 'Bandlaguda')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='class_darja',
            field=models.CharField(choices=[('INTER - I', 'INTER - I'), ('INTER - II', 'INTER - II'), ('B.COM -I', 'B.COM - I'), ('B.COM -II', 'B.COM - II'), ('B.COM -III', 'B.COM - III'), ('Awwal (Alif)', 'اول (الف)'), ('Awwal (Baa)', 'اول (ب)'), ('Awwal (Jeem)', 'اول (ج)'), ('Duwwam (Alif)', 'دوم (الف)'), ('Duwwam (Baa)', 'دوم (ب)'), ('Suwwam (Alif)', 'سوم (الف)'), ('Suwwam (Baa)', 'سوم (ب)'), ('Suwwam (Jeem)', 'سوم (ج)'), ('Chahrum (Alif)', 'چهارم (الف)'), ('Chahrum (Baa)', 'چهارم (ب)'), ('Panjum', 'پنجم'), ('Mouqoof Alai', 'موقوف علیہ'), ('Daur-e-Hadees', 'دورہ حدیث'), ('Edadiya School (Alif)', 'ادادیہ اسکول (الف)'), ('Edadiya School (Baa)', 'ادادیہ اسکول (ب)'), ('Awwal School (Alif)', 'اول اسکول (الف)'), ('Awwal School (Baa)', 'اول اسکول (ب)'), ('Duwwam School (Alif)', 'دوم اسکول (الف)'), ('Duwwam School (Baa)', 'دوم اسکول (ب)'), ('Suwwam', 'سوم'), ('Chahrum', 'چهارم'), ('Hifz-Alif', 'Hifz-Alif'), ('Hifz-Baa', 'Hifz-Baa'), ('Hifz-Jeem', 'Hifz-Jeem'), ('Hifz-Daal', 'Hifz-Daal'), ('Hifz-Zaa', 'Hifz-Zaa'), ('Hifz-Haa', 'Hifz-Haa'), ('Hifz-Haah', 'Hifz-Haah'), ('Hifz-Waav', 'Hifz-Waav'), ('Nazira-Alif', 'Nazira-Alif'), ('Nazira-Baa', 'Nazira-Baa'), ('Nazira-Jeem', 'Nazira-Jeem'), ('Nazira-Daal', 'Nazira-Daal')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.CharField(choices=[('Mahade Ashraf', 'Mahade Ashraf'), ('معہد ابرار', 'معہد ابرار'), ('حفظ', 'حفظ'), ('ناظرہ', 'ناظرہ'), ('معہد علیم', 'معہد علیم'), ('معہد قاسم', 'معہد قاسم')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='monthly_fees',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_type',
            field=models.CharField(choices=[('boarder', 'Boarder'), ('day_scholar', 'Day Scholar')], max_length=20, null=True),
        ),
    ]
