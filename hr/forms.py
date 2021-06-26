from django import forms
from . models import *

class LeaveApplyForm(forms.ModelForm):
    
    class Meta:
        model = LeaveApplication
        fields = ('start_date', 'return_date', 'leave_type')
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'return_date': forms.DateInput(attrs={'type':'date'}),
        }
    
    