from django.urls import path
from .views import (
    UserLoginView,
    DashboardView,
    StaffDashboardView,
    # UserProfileView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("logout/", LogoutView.as_view(), {"next_page": "/"}, name="logout"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # path("profile/crud/<pk>/", CustomerCrudView.as_view(), name="profile-crud"),
    # path("profile/list/", CustomerListView.as_view(), name="profile-list"),
    path("dashboard/staff/", StaffDashboardView.as_view(), name="staff-dashboard"),
    # path("", UserLoginView.as_view()),
    path("", DashboardView.as_view()),
]
