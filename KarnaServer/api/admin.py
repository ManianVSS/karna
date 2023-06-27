import sys

from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.core.exceptions import FieldDoesNotExist
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from import_export.admin import ImportExportModelAdmin
from massadmin.massadmin import MassEditMixin

from .models import Attachment, OrgGroup, Configuration, get_database_name, Resource, Request


@admin.register(Configuration)
class ConfigurationAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'value', ]
    ordering = ('name',)
    list_display = ['name', 'value', ]


def reload_admin_site_name(site_name):
    if site_name is None:
        site_name = "Karna"

        # noinspection PyBroadException
        try:
            site_name = get_database_name()
        except Exception as e:
            print("Defaulting site name Karna as no config data found")

    admin.site.site_header = site_name + " Administration"
    admin.site.site_title = site_name + " Admin Portal"
    admin.site.index_title = "Welcome to " + site_name + " Administration Portal"


# method for updating
@receiver(post_save, sender=Configuration, dispatch_uid="update_admin_site_name")
def update_admin_site_name(sender, instance, **kwargs):
    reload_admin_site_name(None)


if 'runserver' in sys.argv:
    reload_admin_site_name(None)


class CustomModelAdmin(MassEditMixin, ImportExportModelAdmin):
    save_as = True
    readonly_fields = ('id',)

    # ordering = ('-id',)

    # search_fields = ['name', 'summary', 'description', ]

    # noinspection PyProtectedMember
    def get_list_display(self, request):
        return [f.name for f in self.model._meta.get_fields() if f.concrete and
                not (f.many_to_many or f.one_to_many)]
        # return [
        #     f.name if f.model != self.model else None
        #     for f in self.model._meta.get_fields()
        #     if not f.is_relation
        #        or f.one_to_one
        #        or (f.many_to_one and f.related_model)
        # ]

    def has_view_permission(self, request, obj=None):
        if (request is None) or (request.user is None) or request.user.is_superuser or (obj is None):
            return super().has_view_permission(request, obj)
        if super().has_view_permission(request, obj):
            try:
                return not hasattr(obj, 'can_read') or obj.can_read(request.user)
            except FieldDoesNotExist:
                return False
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if (request is None) or (request.user is None) or request.user.is_superuser or (obj is None):
            return super().has_change_permission(request, obj)
        if super().has_change_permission(request, obj):
            try:
                return not hasattr(obj, 'can_modify') or obj.can_modify(request.user)
            except FieldDoesNotExist:
                return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if (request is None) or (request.user is None) or request.user.is_superuser or (obj is None):
            return super().has_delete_permission(request, obj)
        if super().has_delete_permission(request, obj):
            try:
                return not hasattr(obj, 'can_delete') or obj.can_delete(request.user)
            except FieldDoesNotExist:
                return True
        else:
            return False

    # Allow only listing of entities that can be viewed by the user
    def get_queryset(self, request):
        if request.user is None:
            return self.model.objects.none()
        else:
            if (request.method == 'GET') and not request.path.endswith('/change/') and hasattr(self.model,
                                                                                               'get_list_query_set'):
                return self.model.get_list_query_set(self.model, request.user)
            else:
                return self.model.objects.all()
            # return self.model.objects.filter(Q(org_group__isnull=True)
            #                                  | Q(org_group__guests__pk=user_id)
            #                                  | Q(org_group__members__pk=user_id)
            #                                  | Q(org_group__leaders__pk=user_id)
            #                                  ).distinct()


class CustomUserAdmin(CustomModelAdmin, UserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class CustomGroupAdmin(CustomModelAdmin, GroupAdmin):
    pass


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)


@admin.register(Attachment)
class AttachmentAdmin(CustomModelAdmin):
    search_fields = ['name', 'file', ]
    list_filter = (
        'published',
        ('org_group', RelatedOnlyFieldListFilter),
    )


@admin.register(OrgGroup)
class OrgGroupAdmin(CustomModelAdmin):
    list_filter = (
        'published',
        ('org_group', RelatedOnlyFieldListFilter),
        ('leaders', RelatedOnlyFieldListFilter),
        ('members', RelatedOnlyFieldListFilter),
        ('guests', RelatedOnlyFieldListFilter),
    )
    search_fields = ['name', 'summary', 'description', ]


@admin.register(Resource)
class ResourceAdmin(CustomModelAdmin):
    list_filter = (
        'published',
        ('org_group', RelatedOnlyFieldListFilter),
        'type',
    )
    search_fields = ['name', 'summary', 'description', 'purpose', 'type', 'properties', ]


@admin.register(Request)
class RequestAdmin(CustomModelAdmin):
    ordering = ('-id',)
    list_filter = (
        'published',
        ('org_group', RelatedOnlyFieldListFilter),
        'type',
        'start_time',
        'end_time',
        'priority',
        'status'
    )
    search_fields = ['name', 'summary', 'description', 'purpose', 'type', 'properties', ]
