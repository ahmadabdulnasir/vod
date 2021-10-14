#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""

from rest_framework.permissions import BasePermission, IsAdminUser


class IsSuperUser(IsAdminUser):
    allowed_groups = ["SuperUser"]
    message = f"Only users belonging to groups: {allowed_groups} are allowed here"

    def has_permission(self, request, view):
        return (
            True
            if "SuperUser" in [group.name for group in request.user.groups.all()]
            or bool(request.user and request.user.is_superuser)
            else False
        )


class IsICTModerator(BasePermission):
    allowed_groups = ["ICTModerators", "SuperUser"]
    message = f"Only users belonging to groups: {allowed_groups} are allowed here"

    def has_permission(self, request, view):
        # return True if 'ICTModerators' in [group.name for group in request.user.groups.all()] else False
        check = any(
            i in self.allowed_groups
            for i in [group.name for group in request.user.groups.all()]
        )
        return check


class HasActiveCompany(BasePermission):
    """ Check is request user has active profile
    Deny a request with a permission error if the test_func() method returns
    False.
    """

    message = f"Only users with active Company are allowed here"

    def has_permission(self, request, view):
        profile = request.user.profile
        check = bool(
           profile and profile.active and profile.company
        )
        return check


class IsMarkerter(BasePermission):
    allowed_groups = [
        "Markerter",
        "CspSupervisors",
        "RegionalManagers",
        "ICTModerators",
        "SuperUser",
    ]
    message = f"Only users belonging to groups: {allowed_groups} are allowed here"

    def has_permission(self, request, view):
        check = any(
            i in self.allowed_groups
            for i in [group.name for group in request.user.groups.all()]
        )
        return check
