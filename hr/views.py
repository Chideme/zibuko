from hr.models import *
from hr.forms import LeaveApplyForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from datetime import timedelta,datetime

# Create your views here.

# User Authorisation
def hr_approval_groups(user):
    return user.groups.filter(name__in=['hr', 'manager']).exists()


@login_required
def dashboard_view(request):
    

    return render(request, 'hr/dashboard.html')

@login_required
def apply_leave_view(request):
    if request.method == "POST":
        start_date = datetime.strptime(request.POST["start_date"],"%Y-%m-%d")
        return_date = datetime.strptime(request.POST["return_date"],"%Y-%m-%d")
        days_ = (return_date - start_date).days
        form = LeaveApplyForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.employee = request.user
            application.days = days_
            application.approved_by = request.user
            
            application.save()
            form.save_m2m()
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
@user_passes_test(hr_approval_groups)
def awaiting_approvals_view(request):
    
    leave_applications = LeaveApplication.objects.filter(status="False")
    mileage_claims = MileageClaim.objects.filter(status="False")
    salary_advances = SalaryAdvance.objects.filter(status="False")
    expense_claims = ExpenseClaim.objects.filter(status="False")
    return render(request,"hr/awaiting_approval.html",{
        "leave_applications":leave_applications,
        "mileage_claims":mileage_claims,
        "salary_advances":salary_advances,
        "expense_claims":expense_claims
    })



@login_required
@user_passes_test(hr_approval_groups)
def approve_leave_view(request, id):
    if request.method == "POST":
        
        
        id = request.POST["id"]
        action = request.POST["action"]
        application = LeaveApplication.objects.get(pk=id)
        application.status = action
        application.save()
        return HttpResponseRedirect(reverse('hr:awaiting_approval'))
        

    application = LeaveApplication.objects.get(pk=id)
    return render(request,"hr/leave_approval.html",{
        "application":application
    })

@login_required
@user_passes_test(hr_approval_groups)
def approve_mileage_claim_view(request, id):
    if request.method == "POST":
        
        
        id = request.POST["id"]
        
        
        action = request.POST["action"]
        if action != "Open this select menu":
        
            application = MileageClaim.objects.get(pk=id)
            application.status = action
            application.save()
            return HttpResponseRedirect(reverse('hr:awaiting_approval'))
        else:
            return HttpResponseRedirect(reverse('hr:awaiting_approval'))

    application = MileageClaim.objects.get(pk=id)
    return render(request,"hr/mileage_claim.html",{
        "application":application
    })

@login_required
@user_passes_test(hr_approval_groups)
def approve_expense_claim_view(request, id):
    if request.method == "POST":
        
        
        id = request.POST["id"]
        
        
        action = request.POST["action"]
        if action != "Open this select menu":
        
            application = ExpenseClaim.objects.get(pk=id)
            application.status = action
            application.save()
            return HttpResponseRedirect(reverse('hr:awaiting_approval'))
        else:
            return HttpResponseRedirect(reverse('hr:awaiting_approval'))

    application = ExpenseClaim.objects.get(pk=id)
    return render(request,"hr/expense_claim.html",{
        "application":application
    })


@login_required
@user_passes_test(hr_approval_groups)
def approve_salary_advance_view(request, id):
    if request.method == "POST":
        
        
        id = request.POST["id"]
        
        
        action = request.POST["action"]
        if action != "Open this select menu":
        
            application = SalaryAdvance.objects.get(pk=id)
            application.status = action
            application.save()
            return HttpResponseRedirect(reverse('hr:awaiting_approval'))
        else:
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
        application = LunchOrder.objects.create(employee=request.user, order=order.id,amount=order.amount)
        application.save()
        return HttpResponseRedirect(reverse('hr:order_lunch'))
        

    menu = DailyMenu.objects.filter(date=datetime.today)
    return render(request,"hr/place_order.html",{
        "menu":menu
    })