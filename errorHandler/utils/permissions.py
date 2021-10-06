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


class IsRegionalManager(BasePermission):
    allowed_groups = ["RegionalManagers", "ICTModerators", "SuperUser"]
    message = f"Only users belonging to groups: {allowed_groups} are allowed here"

    def has_permission(self, request, view):
        check = any(
            i in self.allowed_groups
            for i in [group.name for group in request.user.groups.all()]
        )
        return check


class IsCSPSupervisor(BasePermission):
    allowed_groups = [
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
