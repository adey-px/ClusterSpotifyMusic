from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('upgrade', views.upgrade, name='upgrade'),
    path('checkout', views.checkout, name='checkout'),
    path('success', views.checkout_success, name='checkout_success'),
    path('download', views.download_access, name='download_access'),
]
