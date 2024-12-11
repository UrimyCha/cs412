from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(r'', views.homepage, name = "homepage"),
    path(r'cats', views.ShowAllCatsView.as_view(), name = "show_all_cats"),
    path(r'menu/', views.menu, name = "menu"),
    path(r'cat/<int:pk>/', views.ShowCatProfile.as_view(), name = "cat_detail"),    
    path(r'reservation/', views.CreateReservationView.as_view(), name = "reservation"),
    path(r'reservation_confirmation/<int:pk>', views.ReservationConfirmView.as_view(), name = "reservation_confirm"),
    path(r'adopt/', views.AdoptionFormView.as_view(), name = "adoption_form"),
    path(r'adoption_confirmation<int:pk>/', views.AdoptionConfirmView.as_view(), name = "adoption_confirm"),
    path(r'reservations/', views.ReservationLookupView.as_view(), name='reservation_lookup'),
    path(r'reservations/update/<int:pk>/', views.ReservationUpdateView.as_view(), name='update_reservation'),
    path(r'reservations/delete/<int:pk>/', views.ReservationDeleteView.as_view(), name='delete_reservation'),

]