from django.urls import path, include
from django.contrib import admin
from rest_framework import routers # type: ignore
from core import views as core_views
from rest_framework.authtoken.views import obtain_auth_token # type: ignore

# Create a router for viewsets
router = routers.DefaultRouter()
router.register('core/transactions', core_views.TransactionViewSet, basename='transactions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the router URLs
    path('api/users/', include('users.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/core/', include('core.urls')),
    path('api/test/', include('testmodel.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
