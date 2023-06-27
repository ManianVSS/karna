from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from .views import UserViewSet, GroupViewSet, AttachmentViewSet, OrgGroupViewSet, ConfigurationViewSet, ResourceViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'configuration', ConfigurationViewSet)
router.register(r'attachments', AttachmentViewSet)

router.register(r'org_groups', OrgGroupViewSet)

router.register(r'resources', ResourceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/restframework', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/jwt/login', jwt_views.TokenObtainPairView.as_view()),
    path('auth/jwt/refresh', jwt_views.TokenRefreshView.as_view()),
]
