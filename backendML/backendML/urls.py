from django.urls import path, include
from django.contrib import admin
from rest_framework import routers # type: ignore
from core import views as core_views
from rest_framework.authtoken.views import obtain_auth_token # type: ignore
from reports import views as reports_views

router = routers.DefaultRouter()
router.register(r'transactions', core_views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the router URLs (if using viewsets)
    path('api/users/', include('users.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/core/', include('core.urls')),  
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # connecting the test-models urls
    path('', reports_views.home, name='home'),
    path('admin/', core_views.admin, name='admin'),
    path('users/', core_views.users, name='users'),
    path('notifications/', core_views.notifications, name='notifications'),
    path('reports/', core_views.reports, name='reports'),
    path('api/contract_parser/', include('contract_parser.urls')),
]
