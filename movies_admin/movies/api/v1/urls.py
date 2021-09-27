from .views import MoviesListApi, MoviesDetailApi
from django.urls import path

urlpatterns = [
    path('movies/', MoviesListApi.as_view()),
    path('movies/<str:pk>', MoviesDetailApi.as_view())
]
