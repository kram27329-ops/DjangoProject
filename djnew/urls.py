from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('add-product/', views.add_product, name='add_product'),

    # Serve media files (works in both dev and production)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)