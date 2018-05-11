from django.urls import path
from lists import views

urlpatterns = [
    path('lists/new', views.new_list, name='new_list'),
    path('lists/the-list', views.view_list, name='view_list'),
    path('lists/add_item', views.add_item, name='add_item')
]