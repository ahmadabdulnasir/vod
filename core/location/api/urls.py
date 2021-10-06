from django.urls import path
from .views import (
    StateList,
    StateDetailsAPIView,
    StateUpdateAPIView,
    StateDeleteAPIView,
    LGACreateAPIView,
    LGAListAPIView,
    LGADetailsAPIView,
    LGAUpdateAPIView,
    LGADeleteAPIView,
)


urlpatterns = [
    path("list/state/", StateList.as_view()),
    path("details/state/<pk>/", StateDetailsAPIView.as_view()),
    path("update/state/<pk>/", StateUpdateAPIView.as_view()),
    path("delete/state/<pk>/", StateDeleteAPIView.as_view()),
    path("create/lga/", LGACreateAPIView.as_view()),
    path("list/lga/", LGAListAPIView.as_view()),
    path("details/lga/<pk>/", LGADetailsAPIView.as_view()),
    path("update/lga/<pk>/", LGAUpdateAPIView.as_view()),
    path("delete/lga/<pk>/", LGADeleteAPIView.as_view()),
]
