from django.urls import path
from . import views

app_name = 'main_page'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('avtomatiz/', views.avtomatiz, name='avtomatiz'),
    path('contacts/', views.contacts, name='contacts'),
    path('reviews/', views.reviews, name='reviews'),
    path('search/', views.search, name='search'),
    path('search_choose/', views.search_choose, name='search_choose'),
]
