from django.urls import path
from .views import ReviewListCreateView, ReviewUpdateDeleteView
urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view(), name="reviews"),
    path('reviews/<int:pk>/', ReviewUpdateDeleteView.as_view(), name="review-delete-update"),
]