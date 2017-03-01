"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler400, handler500
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views


statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

pages = [
    url(r'^$', views.index, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'cardetail', views.car_detail, name='car_detail_page'),
    url(r'userdetail', views.car_detail, name='user_detail_page'),
]

handler400 = 'web.views.bad_request'
handler500 = 'web.views.internal_error'

urlpatterns = pages + statics
