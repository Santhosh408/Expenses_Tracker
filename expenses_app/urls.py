from django.urls import path
from .views import (LogoutView,LoginView,RegisterView,ExpensesView,
                    ExpensesDetailView,UserUpdateView,MonthlyExpenseSummeryView)

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('update/',UserUpdateView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('expenses/',ExpensesView.as_view()),
    path('expenses/<int:pk>/',ExpensesDetailView.as_view()),
    path('monthlyexpenses/',MonthlyExpenseSummeryView.as_view()),
]
