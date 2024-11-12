from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(openapi.Info(
        title="Expenses Tracker API",
        default_version='v1',
        description="API for managing expenses",
        contact=openapi.Contact(email='youremail@gmail.com'),
        license=openapi.License(name="BSD License")),
        permission_classes=[AllowAny],
        public=True,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('expenses_app.urls')),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui')
]
