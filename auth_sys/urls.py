from auth_sys import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.auth_page, name='auth-page'),
    path('register/', views.registration, name='register'),
    path('login/', LoginView.as_view(template_name='auth_sys/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/history/', views.view_history, name='view-history'),
    path('profile/update/', views.profile_update, name='profile-update'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('portfolio/add/', views.portfolio_add, name='portfolio-add'),
    path('portfolio/delete/<int:project_id>/', views.portfolio_delete, name='portfolio-delete'),
    path('portfolio/edit/<int:project_id>/', views.portfolio_edit, name='portfolio-edit'),
]