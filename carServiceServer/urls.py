from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from carService import views

router = routers.DefaultRouter()
router.register(r'districts', views.DistrictViewSet)
router.register(r'addresses', views.AddressViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'users', views.CustomUserViewSet)
router.register(r'analysis', views.OrderAnalysisViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='/api')),
    path('api/users/me/', views.get_me),
    path('api/send/', views.send_notification),
    path('api/test/', views.test_view),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)