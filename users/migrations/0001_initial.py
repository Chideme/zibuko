# Generated by Django 3.2.3 on 2021-06-26 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('swift_code', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeBankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=100)),
                ('account_number', models.BigIntegerField()),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.bank')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_number', models.CharField(max_length=100, null=True)),
                ('national_id', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('leave_days_accrual_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('medical_aid', models.CharField(max_length=100)),
                ('marital_status', models.CharField(max_length=10)),
                ('emergency_contact', models.CharField(max_length=100)),
                ('emergency_contact_cell', models.CharField(max_length=100)),
                ('address', models.TextField(max_length=400)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_approve_hr', 'Approve HR processes'), ('can_view_reports', 'Can view comprehensive reports')),
            },
        ),
    ]
