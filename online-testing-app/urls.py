"""online-testing-app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import include
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views #import this

from register import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('payments.urls', namespace='payments')), # New Url
    path('', include('exams.urls', namespace='exams')),
    path('', include('results.urls', namespace='results')),
    path('register/', v.register, name='register'),
    path('login/password_reset/', v.password_reset, name='password_reset'),
    path('', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
