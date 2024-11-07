<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
=======
from django.urls import path
from .views import GenerateReportView

urlpatterns = [
    path('generate-report/', GenerateReportView.as_view(), name='generate-report'),
]
>>>>>>> e2547b448a2294b3b8149896b509cae05fa862af
