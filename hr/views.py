from django.core.exceptions import ImproperlyConfigured
from hr.models import *
from hr.forms import *
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta,datetime
import pandas as pd

# Create your views here.

# User Authorisation

def hr_approval_groups(user):
    return user.groups.filter(name__in=['hr', 'manager']).exists()


@login_required
def dashboard_view(request):

    leave_applications = LeaveApplication.objects.filter(employee=request.user)
    mileage_claims = MileageClaim.objects.filter(employee=request.user)
    salary_advances = SalaryAdvance.objects.filter(employee=request.user)
    expense_claims = ExpenseClaim.objects.filter(employee=request.user)
    return render(request,"hr/dashboard.html",{
        "leave_applications":leave_applications,
        "mileage_claims":mileage_claims,
        "salary_advances":salary_advances,
        "expense_claims":expense_claims
    })


@login_required
def apply_leave_view(request):
    if request.method == "POST":
        start_date = datetime.strptime(request.POST["start_date"],"%Y-%m-%d")
        return_date = datetime.strptime(request.POST["return_date"],"%Y-%m-%d")
        dd = [start_date + timedelta(days=i) for i in range((return_date - start_date).days +1)]
        
        days_ = len([i for i in dd if i.weekday()< 5])-1

        form = LeaveApplyForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.employee = request.user
            application.days = days_
            application.approved_by = request.user
            
            application.save()
            form.save_m2m()
            messages.success(request, "Applied successfully")
            return HttpResponseRedirect(reverse('hr:apply_leave'))
        else:
            return render(request,"hr/apply_leave.html",{
                "form":form
            }
            )
    form = LeaveApplyForm()
    return render(request,"hr/apply_leave.html",{
        "form":form
    }
    )

@login_required
def apply_mileage_claim_view(request):
    if request.method == "POST":
        opening = float(request.POST["speedometer_opening_reading"])
        closing  = float(request.POST["speedometer_closing_reading"])
        kms = closing-opening
        form = MileageClaimForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.km = kms
            application.employee = request.user
            application.approved_by = request.user
            application.save()
            form.save_m2m()
            messages.success(request, "Submitted successfully")
            return HttpResponseRedirect(reverse('hr:apply_mileage_claim'))
        else:
            return render(request,"hr/apply_mileage_claim.html",{
                "form":form
            }
            )
    form = MileageClaimForm()
    return render(request,"hr/apply_mileage_claim.html",{
        "form":form
    }
    )


@login_required
def apply_expense_claim_view(request):
    if request.method == "POST":
        
        form = ExpenseClaimForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.employee = request.user
            application.approved_by = request.user
            application.save()
            form.save_m2m()
            messages.success(request, "Submitted successfully")
            return HttpResponseRedirect(reverse('hr:apply_expense_claim'))
        else:
            return render(request,"hr/apply_expense_claim.html",{
                "form":form
            }
            )
    form = ExpenseClaimForm()
    return render(request,"hr/apply_expense_claim.html",{
        "form":form
    }
    )


@login_required
def apply_salary_advance_view(request):
    if request.method == "POST":
        
        form = SalaryAdvanceForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.employee = request.user
            application.approved_by = request.user
            application.save()
            form.save_m2m()
            messages.success(request, "Submitted successfully")
            return HttpResponseRedirect(reverse('hr:apply_salary_advance'))
        else:
            return render(request,"hr/apply_salary_advance.html",{
                "form":form
            }
            )
    form = SalaryAdvanceForm()
    return render(request,"hr/apply_salary_advance.html",{
        "form":form
    }
    )

@login_required
@user_passes_test(hr_approval_groups)
def awaiting_approvals_view(request):
    
    leave_applications = LeaveApplication.objects.filter(status="Pending Approval")
    mileage_claims = MileageClaim.objects.filter(status="Pending Approval")
    salary_advances = SalaryAdvance.objects.filter(status="Pending Approval")
    expense_claims = ExpenseClaim.objects.filter(status="Pending Approval")
    return render(request,"hr/awaiting_approval.html",{
        "leave_applications":leave_applications,
        "mileage_claims":mileage_claims,
        "salary_advances":salary_advances,
        "expense_claims":expense_claims
    })



@login_required
def approve_leave_view(request, id):
    if request.method == "POST":
        
        if not hr_approval_groups(request.user):
            messages.error(request, "Not authorised to approve")
            return HttpResponseRedirect(reverse('hr:leave_approval',kwargs={'id':id}))
        id = request.POST["id"]
        action = request.POST["action"]
        application = LeaveApplication.objects.get(pk=id)
        if request.user == application.approved_by:
            messages.error(request, "You can not approve for yourself")
            return HttpResponseRedirect(reverse('hr:leave_approval',kwargs={'id':id}))
        application.status = action
        application.approved_by = request.user
        application.save()
        messages.success(request, "Done")
        return HttpResponseRedirect(reverse('hr:awaiting_approval'))
        

    application = LeaveApplication.objects.get(pk=id)
    return render(request,"hr/leave_approval.html",{
        "application":application
    })

@login_required
def approve_mileage_claim_view(request, id):
    if request.method == "POST":
        # check if user is authorized
        if not hr_approval_groups(request.user):
            messages.error(request, "Not authorised to approve")
            return HttpResponseRedirect(reverse('hr:mileage_approval',kwargs={'id':id}))
        id = request.POST["id"]
        action = request.POST["action"]
        application = MileageClaim.objects.get(pk=id)
        if request.user == application.approved_by:
            messages.error(request, "You can not approve for yourself")
            return HttpResponseRedirect(reverse('hr:mileage_approval',kwargs={'id':id}))
        application.status = action
        application.approved_by = request.user
        application.save()
        messages.success(request, "Done")
        return HttpResponseRedirect(reverse('hr:awaiting_approval'))

    application = MileageClaim.objects.get(pk=id)
    return render(request,"hr/mileage_claim.html",{
        "application":application
    })

@login_required
def approve_expense_claim_view(request, id):
    if request.method == "POST":
        if not hr_approval_groups(request.user):
            messages.error(request, "Not authorised to approve")
            return HttpResponseRedirect(reverse('hr:expense_approval',kwargs={'id':id}))
        id = request.POST["id"]
        action = request.POST["action"]
        application = ExpenseClaim.objects.get(pk=id)
        if request.user == application.approved_by:
            messages.error(request, "You can not approve for yourself")
            return HttpResponseRedirect(reverse('hr:expense_approval',kwargs={'id':id}))
        application.status = action
        application.approved_by = request.user
        application.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(reverse('hr:awaiting_approval'))
    application = ExpenseClaim.objects.get(pk=id)
    return render(request,"hr/expense_claim.html",{
        "application":application
    })


@login_required
def approve_salary_advance_view(request, id):
    if request.method == "POST":
        if not hr_approval_groups(request.user):
            messages.error(request, "Not authorised to approve")
            return HttpResponseRedirect(reverse('hr:advance_approval',kwargs={'id':id}))
        id = request.POST["id"]
        action = request.POST["action"]
        application = SalaryAdvance.objects.get(pk=id)

        if request.user == application.approved_by:
            messages.error(request, "You can not approve for yourself")
            return HttpResponseRedirect(reverse('hr:advance_approval',kwargs={'id':id}))
        application.status = action
        application.approved_by = request.user
        application.save()
        messages.success(request, "Done")
        return HttpResponseRedirect(reverse('hr:awaiting_approval'))

    application = SalaryAdvance.objects.get(pk=id)
    return render(request,"hr/salary_advance.html",{
        "application":application
    })


@login_required
def order_lunch_view(request):
    if request.method == "POST":
        
        
        order_id = int(request.POST["order"])
        order = Menu.objects.get(order_id)
        date = request.POST["date"]
        app = LunchOrder.objects.filter(date=date,employee=request.user)
        if app:
            application = LunchOrder.objects.create(employee=request.user, order=order.id,amount=order.price)
        else:
            application = LunchOrder.objects.create(employee=request.user, order=order.id,amount=order.employee_deduction_amount)
        application.save()
        messages.success(request, "Order placed")
        return HttpResponseRedirect(reverse('hr:order_lunch'))
        
    t = datetime.strftime(datetime.today(),"%Y-%m-%d")
    daily_menu = DailyMenu.objects.filter(date=t)

    return render(request,"hr/place_order.html",{
        "orders":daily_menu
    })


@login_required
@user_passes_test(hr_approval_groups)
def process_lunch_orders_view(request):
    if request.method == "POST":
        
        id = request.POST["id"]
        action = request.POST["action"]
        order = LunchOrder.objects.get(pk=id)
    
        order.status = action
        order.prossed_by = request.user
        order.save()
        return HttpResponseRedirect(reverse('hr:process__lunch_orders'))
        

    orders = LunchOrder.objects.filter(status="Pending Approval")
    return render(request,"hr/process_lunch_orders.html",{
        "orders": orders
    })

