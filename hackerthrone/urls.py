"""
URL configuration for hackerthrone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from FraudDetectionApp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("loan-application/", loan_application_view, name="loan-application"),
    path("fraud-application/", credit_card_fraud_view, name="fraud-application"),
    path(
        "gold-price-application/",
        gold_price_prediction_view,
        name="gold-price-prediction",
    ),
    path(
        "bitcoin/",
        bitcoin_price_prediction_view,
        name="bitcoin-price-prediction",
    ),
    path("service/", service, name="service"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
