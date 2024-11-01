from django.urls import path, include
from django.contrib import admin
from rest_framework import routers # type: ignore
from core import views as core_views
from rest_framework.authtoken.views import obtain_auth_token # type: ignore

router = routers.DefaultRouter()
router.register(r'transactions', core_views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the router URLs (if using viewsets)
    path('api/users/', include('users.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/core/', include('core.urls')),  # Ensure the trailing slash is present
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # connecting the test-models urls
    path('api/', include('testmodel.urls'))
]
