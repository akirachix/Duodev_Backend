from django.urls import path
from . import views

app_name = 'textilebale'

urlpatterns = [
    path('post/', views.post_textile_bale, name='post_textile_bale'),
   
]
