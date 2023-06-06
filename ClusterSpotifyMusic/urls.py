"""cluster URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),  # from allauth web
    path("", include("home.urls")),  # Home app url for home page
    path("music/", include("music.urls")),  # All urls in music app
    path("profiles/", include("profiles.urls")),  # All urls in music app
    path("checkout/", include("checkout.urls")),
    path("public/", include("public.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
