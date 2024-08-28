from django.urls import path

from account.views import RegisterView, LoginView

urlpatterns = [
  path('account_register/', RegisterView.as_view()),
  path('login/', LoginView.as_view()),
]