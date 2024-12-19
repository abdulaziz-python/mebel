from django.urls import path
from . import views

urlpatterns = [
    path('furniture/', views.FurnitureListView.as_view(), name='furniture-list'),
    path('furniture/<str:furniture_id>/', views.FurnitureDetailView.as_view(), name='furniture-detail'),
]