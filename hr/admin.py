from hr.models import Menu
from django.contrib import admin
from hr.models import *

# Register your models here.
admin.site.register(LeaveApplication)
admin.site.register(LeaveAdjustment)
admin.site.register(MenuItem)
admin.site.register(Menu)
admin.site.register(DailyMenu)
admin.site.register(MileageRate)
admin.site.register(EmployeeVehicle)


