from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Attachment, OrgGroup, Configuration


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'url', 'name']


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['id', 'name', 'value']


class OrgGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgGroup
        fields = ['id', 'name', 'summary', 'auth_group', 'description', 'org_group', 'leaders', 'published', ]


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'name', 'file', 'org_group', 'published', ]
