from django.urls import path
# from api.views import GoogleLogin
from api.views import HomeView

urlpatterns = [
    # path("rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("home/", HomeView.as_view(), name="home"),
]