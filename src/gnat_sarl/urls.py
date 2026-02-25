
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home_app.urls")),
]


if settings.DEBUG:
    #include django_browser_reload URLS only DEBUG mode
    urlpatterns +=[
        path("__reload__/", include("django_browser_reload.urls")),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)