from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('faq/', views.faq, name='faq'),
    path('feedback/', views.feedback, name='feedback'),
]
