from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("backend/admin/", admin.site.urls),
    path("backend/api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "backend/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "backend/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
    # path('backend/api/', include('transit_managment.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += [
        path("backend/silk/", include("silk.urls", namespace="silk")),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
