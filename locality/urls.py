"""geo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from locality import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.world, name='world'),
    path('<int:geonameid>-<str:slug>', views.loc, name="loc"),
    path('<str:country_code>', views.country, name="country"),
    path('<str:country_code>/<str:aa1_code>', views.aa1, name="aa1"),
    path('<str:country_code>/<str:aa1_code>/<str:aa2_code>', views.aa2, name="aa2")
]
