"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib import admin
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('properties/', PropertyListView.as_view(), name='property-list'),
    path('properties/<int:id>/', PropertyDetailView.as_view(), name='property-detail'),

    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('faq/', FAQView.as_view(), name='faq-list'),
    path('contact/', ContactView.as_view(), name='contact_us'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('services/', ServiceView.as_view(), name='services'),

]
