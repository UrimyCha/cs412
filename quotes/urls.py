from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [    
    path(r'', views.quote, name = "quote"),  #have to match views w/ home
    path(r'about', views.about, name = "about"),
    path(r'show_all', views.show_all, name = "show_all")
]
