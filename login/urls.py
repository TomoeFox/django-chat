from django.urls import path
from login import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', login_required(views.DashboardView.as_view()), name='dashboard'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
]