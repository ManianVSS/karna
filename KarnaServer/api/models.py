from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from main import settings


class Configuration(models.Model):
    name = models.CharField(max_length=256, unique=True)
    value = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name) + ": " + str(self.value)


def get_database_name():
    database_name_config = Configuration.objects.filter(name="name")
    if database_name_config.count() > 0:
        return database_name_config[0].value
    return "Karna"


# noinspection PyMethodMayBeStatic
class BaseModel(models.Model):
    class Meta:
        abstract = True

    published = models.BooleanField(default=False, verbose_name='is published content')

    def __str__(self):
        if hasattr(self, 'name'):
            string_value = str(self.name)
            if hasattr(self, 'summary'):
                if self.summary is not None:
                    string_value = string_value + ":" + str(self.summary)
        else:
            string_value = str(self.id)
        return string_value

    def is_guest(self, user):
        return user is not None

    def is_member(self, user):
        return user is not None

    def is_owner(self, user):
        return user is not None

    def can_read(self, user):
        return self.is_owner(user) or self.is_member(user) or self.is_guest(user)

    def can_modify(self, user):
        return self.is_owner(user) or self.is_member(user)

    def can_delete(self, user):
        return self.is_owner(user)

    def get_list_query_set(self, user):
        return self.objects.all()


# noinspection PyUnresolvedReferences
class OrgGroup(BaseModel):
    name = models.CharField(max_length=256, unique=True)
    auth_group = models.OneToOneField(Group, null=True, blank=True, on_delete=models.SET_NULL, related_name="org_group",
                                      verbose_name='authorization group')
    summary = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    org_group = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name="sub_org_groups", verbose_name='parent organization group')
    leaders = models.ManyToManyField(User, blank=True, related_name="org_group_where_leader")
    members = models.ManyToManyField(User, blank=True, related_name="org_group_where_member")
    guests = models.ManyToManyField(User, blank=True, related_name="org_group_where_guest")

    def is_owner(self, user):
        return (self.leaders is not None) and (user in self.leaders.all())

    def is_member(self, user):
        return (self.members is not None) and (user in self.members.all())

    def is_guest(self, user):
        return (self.guests is not None) and (user in self.guests.all())

    def get_list_query_set(self, user):
        user_id = user.id if user else None
        if user.is_superuser:
            return self.objects.all()
        return self.objects.filter(Q(guests__pk=user_id)
                                   | Q(members__pk=user_id)
                                   | Q(leaders__pk=user_id)
                                   ).distinct()


# noinspection PyUnresolvedReferences
class OrgModel(BaseModel):
    class Meta:
        abstract = True

    org_group = models.ForeignKey(OrgGroup, on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name='organization group')

    def is_owner(self, user):
        return (self.org_group is None) or self.org_group.is_owner(user)

    def is_member(self, user):
        return (self.org_group is None) or self.org_group.is_member(user)

    def is_guest(self, user):
        return (self.org_group is None) or self.org_group.is_guest(user)

    def can_read(self, user):
        return (self.org_group is None) or self.is_owner(user) or self.is_member(user) or self.is_guest(user)

    def can_modify(self, user):
        return (self.org_group is None) or self.is_owner(user) or self.is_member(user)

    def can_delete(self, user):
        return (self.org_group is None) or self.is_owner(user)

    def get_list_query_set(self, user):
        if user.is_superuser:
            return self.objects.all()
        user_id = user.id if user else None
        return self.objects.filter(Q(org_group__isnull=True)
                                   | Q(org_group__guests__pk=user_id)
                                   | Q(org_group__members__pk=user_id)
                                   | Q(org_group__leaders__pk=user_id)
                                   ).distinct()


class ReviewStatus(models.TextChoices):
    DRAFT = 'DRAFT', _('Draft'),
    IN_PROGRESS = 'IN_PROGRESS', _('In progress'),
    IN_REVIEW = 'IN_REVIEW', _('In Review'),
    APPROVED = 'APPROVED', _('Approved'),


class Attachment(OrgModel):
    org_group = models.ForeignKey(OrgGroup, on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name='organization group', related_name='api_attachments')
    name = models.CharField(max_length=256)
    file = models.FileField(upload_to=settings.MEDIA_BASE_NAME, blank=False, null=False)
