from auth_sys import views
from django.urls import path

# urlpatterns = [
#     path('test', views.TestUsersView.as_view(), name='test'),
# ]

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]