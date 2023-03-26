from django.contrib import admin
from django.urls import path
from validator_for_mctoptwp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('index/validate', views.validate, name='validate'),
]
