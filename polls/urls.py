from django.contrib import admin
from django.urls import path, include

from .views import index, site_map, csrf_attack


urlpatterns = [
    path('', index, name='index'),
    path('map/', site_map, name='site_map'),
    path('polls/', include('core.urls'), name='core'),
    path('registration/', include('registration.urls'), name='registration'),
    path('admin/', admin.site.urls),
    path('csrf_attack/', csrf_attack, name='csrf_attack'),
]
