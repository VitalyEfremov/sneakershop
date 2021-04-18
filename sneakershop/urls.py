from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from shop.views import contacts_view, about_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('user/', include('users.urls')),
    path('contacts/', contacts_view, name='contacts'),
    path('about/', about_view, name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
