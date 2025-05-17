from .views import ProjectsToBid
from django.urls import path
urlpatterns = [
    path('projects/', ProjectsToBid.as_view(), name='projects_to_bid')
]