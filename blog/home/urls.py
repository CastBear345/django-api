from django.urls import path, include
from home.views import PostView, PublicPost

urlpatterns = [
  path('', PublicPost.as_view()),
  path('details/', PostView.as_view()),
]