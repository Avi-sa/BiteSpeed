from django.urls import path
from .views import *

urlpatterns = [
    path(r"identify/", IdentifyAPIView.as_view(), name="identify")
]
