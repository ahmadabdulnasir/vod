from django.urls import path
from .views import HomeView, MainPageDetailView, contactView, SettingsListView, SettingsEditAddView

# app_name = 'core'

urlpatterns = [
    path("p/<str:slug>/", MainPageDetailView.as_view(), name="page"),
    path("contact/", contactView, name="contact"),
    path("settings/list/", SettingsListView.as_view(), name="core-settings-list"),
    path("settings/edit/<pk>/", SettingsEditAddView.as_view(), name="core-settings-edit-add"),
    path("", HomeView.as_view(), name="home"),
]
