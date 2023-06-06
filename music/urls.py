from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('playing/<audio_id>/', views.now_playing, name='now_playing'),
    path('not_playing/', views.not_playing, name='not_playing'),
    path('add_audio/', views.add_audio, name='add_audio'),
    path('edit_audio/<audio_id>', views.edit_audio, name='edit_audio'),
    path('delete/<audio_id>', views.delete_audio, name='delete_audio'),
    path('my_audio/', views.my_audio, name='my_audio'),
    path('favourite/<audio_id>', views.save_audio, name='save_audio'),
    path('saved_audio/', views.view_saved_audio, name='view_saved_audio'),
    path('history/', views.history, name='history'),
    path('share/', views.share_audio, name='share_audio'),
    path('manage_product/', views.manage_product,
         name='manage_product'),
]
