from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
    # creating a subclass of the generic view ListView
    path(r'', views.ShowAllView.as_view(), name = "show_all")
]
