from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('bmi/', views.bmi_input_view, name='bmi_input'),
    path('bmi/result/', views.bmi_result_view, name='bmi_result'),
    path('bmi/download/', views.download_bmi_diet, name='download_bmi_diet'),
]
