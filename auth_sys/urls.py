from auth_sys import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.AuthPageView.as_view(), name='auth-page'),
    path('register/', views.registration, name='register'),
    path('login/', LoginView.as_view(template_name='auth_sys/login.html', redirect_authenticated_user = True), name='login'),
    path('logout/', views.logout_view, name='logout'),


    path('profile/<str:username>', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile-update'),
    path('profile/change-password/', views.change_password, name='change-password'),
    path('profile/change-avatar/', views.change_avatar, name='change-avatar'),
    path('profile/change-email/', views.change_email, name='change-email'),
    path('profile/change-phone-number/', views.change_phone_number, name='change-phone-number'),
    path('profile/change-description/', views.change_description, name='change-description'),
]