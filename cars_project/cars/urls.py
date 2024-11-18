from django.urls import path

from .views import *

urlpatterns = [
    path('my_records/', MyRecordsView.as_view(), name='my_records'),
    path('api/cars/', CarListAPIView.as_view()),
    path('api/cars/<int:pk>/', CarDetailAPIView.as_view()),
    path('api/cars/<int:pk>/comments/', CommentListAPIView.as_view()),
    ##########################

    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/add/', CarAddView.as_view(), name='car_add'),
    path('cars/<int:pk>/edit/', CarEditView.as_view(), name='car_edit'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    # path('cars/<int:pk>/comments/add/', CommentAddView.as_view(), name='comment_add'),

]
