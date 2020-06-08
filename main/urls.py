from django.urls import path
from .views import (
    homeView,
    api_to_database,
)


app_name = "main"
urlpatterns = [
    path('', homeView, name="home"),
    path('api-call/', api_to_database, name="api_call"),
]
