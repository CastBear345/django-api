from django.urls import path, include
from home.views import PostView, PublicPost

urlpatterns = [
  ##path('', PostView.as_view()),
  path('add/', PostView.as_view()),
  path('all/', PublicPost.as_view()),
]