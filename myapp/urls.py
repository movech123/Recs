from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Serves the HTML page
    path('get-recommendations/', views.get_recommendations, name='get_recommendations'),
    path('submit-rating/', views.submit_rating, name='submit-rating'),
]