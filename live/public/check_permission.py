# -*- coding: utf-8 -*-

from rest_framework import permissions

from django.contrib.auth.models import Group

# from user.models import TYPE_USER_STAR


class SystemPermission(permissions.BasePermission):
    '''
    超级管理员
    '''
    def has_permission(self, request, view):
        if not request.auth:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return True


class AdminPermission(permissions.BasePermission):
    '''
    系统管理组
    '''
    def has_permission(self, request, view):
        if not request.auth:
            return False

        if request.user.is_superuser:
            return True

        # if request.method in permissions.SAFE_METHODS:
        #     return True

        try:
            group_admin = Group.objects.get(name='admin')
        except:
            return False

        if request.user and group_admin in request.user.groups.all():
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        try:
            group_admin = Group.objects.get(name='admin')
        except:
            return False

        if request.user and group_admin in request.user.groups.all():
            return True

        return False


class StaffPermission(permissions.BasePermission):
    '''
    运营组
    '''
    def has_permission(self, request, view):
        if not request.auth:
            return False

        if request.user.is_superuser:
            return True

        groups = Group.objects.filter(name__in=['staff', 'admin'])

        if request.user:
            user_group = request.user.groups.all()
            if len(user_group) == 1 and user_group.first() in groups:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        groups = Group.objects.filter(name__in=['staff', 'admin'])

        if request.user:
            user_group = request.user.groups.all()
            if len(user_group) == 1 and user_group.first() in groups:
                return True

        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if not request.auth:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj == request.user


class OwnerPermission(permissions.BasePermission):
    """
    只有拥有者才能操作
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return False

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner_user == request.user


class StarPermission(permissions.BasePermission):
    """
    只有大咖才能创建问卷类对象
    """
    def has_permission(self, request, view):
        if not request.auth:
            return False

        user = request.user
        # 避免有些数据user_info没有跟auth_user建立关系
        if not hasattr(user, 'owner'):
            return False

        user_info = request.user.owner
        if not user_info:
            return False
        if request.method in ['POST', 'PUT', 'PATCH']:
            # if user_info.type == TYPE_USER_STAR:
            return True
        return False


class StarOrStaffPermission(permissions.BasePermission):
    '''
    老师，运营
    '''
    def has_permission(self, request, view):
        if not request.auth:
            return False

        if request.user.is_superuser:
            return True

        groups = Group.objects.filter(name__in=['staff', 'admin'])

        if request.user:
            user_group = request.user.groups.all()
            if len(user_group) == 1 and user_group.first() in groups:
                return True

        user_info = request.user.owner
        if not user_info:
            return False
        # if user_info.type == TYPE_USER_STAR:
            return True
        return False

