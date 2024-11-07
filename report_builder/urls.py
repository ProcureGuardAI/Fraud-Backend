from django.urls import path
from. import views

urlpatterns = [
    path('generate_report/', views.generate_report, name='generate_report'),
#    path('schedule_report/', views.schedule_report, name='schedule_report'),
]