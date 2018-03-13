# -*- coding: utf-8 -*-


from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PttSerializer(serializers.Serializer):
    post_time = serializers.CharField(required=True, max_length=50)
    title = serializers.CharField(required=True, max_length=100)
    content = serializers.CharField(required=False, max_length=200)
