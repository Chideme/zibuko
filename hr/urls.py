from django.urls import path

from . import views

app_name ='hr'
urlpatterns = [
    path("Dashboard/",views.dashboard_view, name='dashboard'),
    path("ApplyLeave/",views.apply_leave_view, name='apply_leave'),
    path("LeaveApproval/<int:id>",views.approve_leave_view, name='leave_approval'),
    path("MileageApproval/<int:id>",views.approve_mileage_claim_view, name='mileage_approval'),
    path("ExpenseApproval/<int:id>",views.approve_expense_claim_view, name='expense_approval'),
    path("AdvanceApproval/<int:id>",views.approve_salary_advance_view, name='advance_approval'),
    path("AwaitingApprovals/",views.awaiting_approvals_view, name='awaiting_approval'),
    path("OrderLunch/",views.dashboard_view, name='order_lunch')
]
    