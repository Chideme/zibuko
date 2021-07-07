from users.models import Employee
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.conf.urls.static import static
from django.utils import timezone
from datetime import date, time

# Create your models here.


class LeaveApplication(models.Model):
    date = models.DateField(default=timezone.now)
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='employee',null=False)
    start_date = models.DateField(null=False,default=timezone.now)
    return_date = models.DateField(default=timezone.now)
    LEAVE_TYPE_CHOICES = [
        ('Annual', 'Annual'),
        ('Sick', 'Sick'),
        ('Study', 'Study'),
        ('Other', 'Other'),
    ]
    leave_type = models.CharField(max_length=100,choices=LEAVE_TYPE_CHOICES,default="Annual",null=False)
    days = models.DecimalField(max_digits=5,decimal_places=2,null=False)
    status = models.CharField(max_length=100,default="Pending Approval") #change column to status
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='supervisor',null=True)


class LeaveAdjustment(models.Model):
    date = models.DateField(null=False,default=timezone.now)
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+',null=False)
    reason = models.CharField(max_length=100,null=False)
    days = models.DecimalField(max_digits=5,decimal_places=2,null=False)
    adjusted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='adjuster',null=False)

class Menu(models.Model):
    name= models.CharField(max_length=100,null=False) 
    price = models.DecimalField(max_digits=6,decimal_places=2,null=False)
    employee_deduction_amount = models.DecimalField(max_digits=6,decimal_places=2,null=False)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name= models.CharField(max_length=100,null=False)
    category =models.CharField(max_length=100,null=False)
    menu= models.ForeignKey(Menu, on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return self.name


class DailyMenu(models.Model):
    date = models.DateField(default=timezone.now)
    menu_item= models.ForeignKey(MenuItem, on_delete=models.CASCADE,null=False)
    menu= models.ForeignKey(Menu, on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return self.menu.name

class LunchOrder(models.Model):
    date = models.DateField(null=False,default=timezone.now)
    employee = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    order = models.ForeignKey(Menu, on_delete=models.CASCADE,null=False)
    amount = models.DecimalField(max_digits=5,decimal_places=2,null=False)
    status = models.CharField(max_length=100,default="Pending Approval")
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='lunch_clerk',null=False,default="Kuda")

class SalaryAdvance(models.Model):
    date = models.DateField(null=False,default=timezone.now)
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='emp',null=False)
    amount= models.DecimalField(max_digits=6,decimal_places=2,null=False)
    status = models.CharField(max_length=100,default="Pending Approval")
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='manager',null=False)

class ExpenseClaim(models.Model):
    date = models.DateField(default=timezone.now)
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='claimer')
    amount= models.DecimalField(max_digits=6,decimal_places=2)
    expense = models.CharField(max_length=100) 
    status = models.CharField(max_length=100,default="Pending Approval")
    receipt = models.FileField(upload_to='claims/',validators=[FileExtensionValidator(allowed_extensions=['pdf'])],help_text='Select a pdf file')  
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='claim_approver')


class MileageRate(models.Model):
    vehicle_type = models.CharField(max_length=100) 
    fuel_engine_type = models.CharField(max_length=100,null=False)
    mileage_rate= models.DecimalField(max_digits=6,decimal_places=2) 
    total_cost_rate= models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return "Vehicle: {}, Engine: {} ".format(self.vehicle_type,self.fuel_engine_type)

class EmployeeVehicle(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='vehicle_owner')
    name = models.CharField(max_length=100,null=False)
    registration_number =  models.CharField(max_length=100,null=False)
    mileage_type = models.ForeignKey(MileageRate, on_delete=models.CASCADE,null=False)

    def __str__(self):
        return self.name

class MileageClaim(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='mileage_claimer')
    date = models.DateField(null=False,default=timezone.now)
    time_in = models.TimeField(null=False)
    time_out = models.TimeField(null=False)
    details = models.TextField(max_length=100,null=False)#trip details
    employee_vehicle = models.ForeignKey(EmployeeVehicle, on_delete=models.CASCADE,null=False)
    speedometer_opening_reading =  models.DecimalField(max_digits=9,decimal_places=2)
    speedometer_closing_reading = models.DecimalField(max_digits=9,decimal_places=2)
    km= models.DecimalField(max_digits=9,decimal_places=2,null=False)
    status = models.CharField(max_length=100,default="Pending Approval")
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='mileage_approver')  