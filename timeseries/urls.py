from django.urls import path
from .views import *
urlpatterns = [
    path('', simulator.as_view()),
    path('run/',simulator.run)

]
