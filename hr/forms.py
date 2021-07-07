from django import forms
from django.core.exceptions  import ValidationError
from . models import *





class LeaveApplyForm(forms.ModelForm):
    
    class Meta:
        model = LeaveApplication
        fields = ('start_date', 'return_date', 'leave_type')
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'return_date': forms.DateInput(attrs={'type':'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        return_date = cleaned_data.get('return_date')
        if start_date >= return_date:
            raise ValidationError("Return date can not be before start date")
        

    

class MileageClaimForm(forms.ModelForm):
    
    class Meta:
        model = MileageClaim
        fields = ('date', 'time_in', 'time_out', 'details', 'employee_vehicle',
                'speedometer_opening_reading', 'speedometer_closing_reading')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'time_in': forms.TimeInput(attrs={'type':'time'}),
            'time_out': forms.TimeInput(attrs={'type':'time'}),
        }


class ExpenseClaimForm(forms.ModelForm):
    
    class Meta:
        model = ExpenseClaim
        fields = ('date', 'amount', 'expense', 'receipt')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'receipt': forms.FileInput(attrs={'type':'file'})
        }

class SalaryAdvanceForm(forms.ModelForm):
    
    class Meta:
        model = SalaryAdvance
        fields = ('date', 'amount')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
        }
    