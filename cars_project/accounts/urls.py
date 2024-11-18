from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ######
    path('api/register/', RegisterAPIView.as_view()),
    path('api/login/', LoginAPIView.as_view()),
]
