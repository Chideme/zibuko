from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="staff")
    staff_number = models.CharField(max_length=100,null=True)
    national_id = models.CharField(max_length=100,null=False)
    department = models.CharField(max_length=100,null=False,default="Zibuko")
    position = models.CharField(max_length=100,null=False)
    start_date = models.DateField(null=False)
    leave_days_accrual_rate = models.DecimalField(max_digits=5,decimal_places=2,null=False)
    medical_aid =  models.CharField(max_length=100)
    marital_status = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=100,null=False)
    emergency_contact_cell = models.CharField(max_length=100,null=False)
    address = models.TextField(max_length=400,null=False)

    class Meta:
         
        permissions = (
            ('can_approve_hr', 'Approve HR processes'),
            ('can_view_reports', 'Can view comprehensive reports')    
        )



class Bank(models.Model):
    name = models.CharField(max_length=100,null=False,unique=True) 
    swift_code =  models.CharField(max_length=100,unique=True) 

class EmployeeBankDetails(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE,null=False)
    branch = models.CharField(max_length=100,null=False) 
    account_number= models.BigIntegerField(null=False)
    