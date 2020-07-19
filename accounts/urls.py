from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('edit/', views.edit, name='edit'),
    path('logout/', views.user_logout, name='logout'),
]
