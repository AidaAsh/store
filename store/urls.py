
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

from crud import views
from store import settings

schema_view = get_schema_view(
    openapi.Info(
        title="test task project api",
        default_version='v1',
        description="For LMS project rest api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="a.eshkozieva13@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

router = DefaultRouter()
router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'purchase', views.PurchasesViewSet, basename='purchases')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'balance', views.BalanceViewSet, basename='balance')
router.register(r'note', views.NotificationsViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
