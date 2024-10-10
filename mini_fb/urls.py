from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
    # creating a subclass of the generic view ListView
    path(r'', views.ShowAllProfilesView.as_view(), name = "show_all_profiles"),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name = "show_profile"),
    path(r'create_profile', views.CreateProfileView.as_view(), name = "create_profile")

]
