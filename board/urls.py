from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.board_list),
    path('write/', views.board_write),
    path('detail/<int:pk>/', views.board_detail),
    path('edit/<int:pk>/', views.board_edit),
    path('delete/<int:pk>/', views.board_delete),
]