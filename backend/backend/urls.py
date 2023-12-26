
from django.contrib import admin
from django.urls import path, include
from Admin import urls as admin_urls
from Restaurants import urls as restaurant_urls
from Diners import urls as diners_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include(admin_urls)),
    path('restaurants/', include(restaurant_urls)),
    path('diners/', include(diners_urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
