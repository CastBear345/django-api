from django.urls import path, include
from home.views import PostView

urlpatterns = [
  ##path('', PostView.as_view()),
  path('add/', PostView.as_view()),
]