from django.contrib.auth.models import User, Group
from django.core.exceptions import FieldDoesNotExist
from rest_framework import viewsets
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Attachment, OrgGroup, Configuration, Resource
from .serializers import UserSerializer, GroupSerializer, AttachmentSerializer, OrgGroupSerializer, \
    ConfigurationSerializer, ResourceSerializer

exact_fields_filter_lookups = ['exact', ]
# many_to_many_id_field_lookups = ['contains']
id_fields_filter_lookups = ['exact', 'in', ]
string_fields_filter_lookups = ['exact', 'iexact', 'icontains', 'regex', ]
# 'startswith', 'endswith', 'istartswith','iendswith', 'contains',
compare_fields_filter_lookups = ['exact', 'lte', 'lt', 'gt', 'gte', ]
date_fields_filter_lookups = ['exact', 'lte', 'gte', 'range', ]
# date,year, month, day, week, week_day, iso_week, iso_week_day, quarter
datetime_fields_filter_lookups = ['exact', 'lte', 'gte', 'range', ]
# time, hour, minute, second
default_search_fields = ['name', 'summary', 'description', ]
default_ordering = ['id', ]


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class DjangoObjectPermissionsOrAnonReadOnly(DjangoObjectPermissions):
    """
    Similar to DjangoObjectPermissions, except that anonymous users are
    allowed read-only access.
    """
    authenticated_users_only = False


class KarnaOrgGroupViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        model = self.queryset.model
        if (self.action == 'list') and hasattr(model, 'get_list_query_set'):
            return model.get_list_query_set(model, self.request.user)
        else:
            return super().get_queryset()


class KarnaOrgGroupObjectLevelPermission(DjangoModelPermissions):
    # authenticated_users_only = False

    def has_object_permission(self, request, view, obj):
        # if request.method in SAFE_METHODS:
        #     return True

        # if not super().has_object_permission(request, view, obj):
        #     return False

        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user

        match request.method:
            case 'HEAD' | 'OPTIONS':
                return super().has_object_permission(request, view, obj)
            case 'GET':
                try:
                    return not hasattr(model_cls, 'can_read') or model_cls.can_read(obj, request.user)
                except FieldDoesNotExist:
                    return False
            case 'POST':
                return True
            case 'PUT' | "PATCH":
                try:
                    return not hasattr(model_cls, 'can_modify') or model_cls.can_modify(obj, request.user)
                except FieldDoesNotExist:
                    return False
            case _:
                try:
                    return not hasattr(model_cls, 'can_delete') or model_cls.can_delete(obj, request.user)
                except FieldDoesNotExist:
                    return False
        return True


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
    search_fields = ['id', 'username', 'first_name', 'last_name', 'email']
    ordering_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', ]
    ordering = default_ordering
    filterset_fields = {
        'id': id_fields_filter_lookups,
        'username': string_fields_filter_lookups,
        'first_name': string_fields_filter_lookups,
        'last_name': string_fields_filter_lookups,
        'email': string_fields_filter_lookups,
        'is_staff': exact_fields_filter_lookups,
        'is_active': exact_fields_filter_lookups,
        'date_joined': date_fields_filter_lookups,
    }


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsSuperUser]
    search_fields = ['id', 'name', ]
    ordering_fields = ['id', 'name', ]
    ordering = default_ordering
    filterset_fields = {
        'id': id_fields_filter_lookups,
        'name': string_fields_filter_lookups,
        'permissions': id_fields_filter_lookups,
    }


# filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)


class ConfigurationViewSet(ModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    permission_classes = [IsSuperUser]
    search_fields = ['name', 'value']
    ordering_fields = ['id', 'name']
    ordering = ['name']
    filterset_fields = {
        'id': id_fields_filter_lookups,
        'name': string_fields_filter_lookups,
        'value': string_fields_filter_lookups,
    }


class OrgGroupViewSet(KarnaOrgGroupViewSet):
    queryset = OrgGroup.objects.all()
    serializer_class = OrgGroupSerializer
    permission_classes = [KarnaOrgGroupObjectLevelPermission]
    search_fields = default_search_fields
    ordering_fields = ['id', 'name', 'auth_group', 'org_group', 'leaders', 'published', ]
    ordering = default_ordering
    filterset_fields = {
        'id': id_fields_filter_lookups,
        'name': string_fields_filter_lookups,
        'summary': string_fields_filter_lookups,
        'auth_group': id_fields_filter_lookups,
        'org_group': id_fields_filter_lookups,
        'leaders': exact_fields_filter_lookups,
        'members': exact_fields_filter_lookups,
        'guests': exact_fields_filter_lookups,
        'published': exact_fields_filter_lookups,
    }


class AttachmentViewSet(KarnaOrgGroupViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [KarnaOrgGroupObjectLevelPermission]
    search_fields = default_search_fields
    ordering_fields = ['id', 'name', 'org_group', 'published', ]
    ordering = default_ordering
    filterset_fields = {
        'id': id_fields_filter_lookups,
        'name': string_fields_filter_lookups,
        'org_group': id_fields_filter_lookups,
        'published': exact_fields_filter_lookups,
    }


class ResourceViewSet(KarnaOrgGroupViewSet):
    queryset = Resource.objects.filter(published=True)
    serializer_class = ResourceSerializer
    permission_classes = [KarnaOrgGroupObjectLevelPermission]
    search_fields = default_search_fields
    ordering_fields = ['id', 'name', 'summary', 'type', 'purpose', 'org_group', 'published', ]
    ordering = default_ordering
    filterset_fields = {
        'id': id_fields_filter_lookups,
        'name': string_fields_filter_lookups,
        'summary': string_fields_filter_lookups,
        'type': string_fields_filter_lookups,
        'purpose': string_fields_filter_lookups,
        'org_group': id_fields_filter_lookups,
        'published': exact_fields_filter_lookups,
    }
