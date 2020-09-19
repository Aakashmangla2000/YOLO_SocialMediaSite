from django.urls import path

from social import views

urlpatterns = [
    path('home/', views.Home.as_view()),
    path('post/', views.Post.as_view()),
    path('post/<int:pk>/like', views.PostLike),
    path('', views.Wall.as_view()),
]