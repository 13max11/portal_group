from auth_sys import views
from django.urls import path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('register/', views.RegistationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='auth_sys/login.html', redirect_authenticated_user = True), name='login'),
]