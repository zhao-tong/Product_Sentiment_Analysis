from django.urls import path

from . import views

app_name = 'plot'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/search&load/', views.search_and_load, name='search&load'),
]
