from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.urls import include, path, re_path
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path("", include("home.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("apps.api.urls")),
    path("users/", include("apps.users.urls")),
    path("question/", include("apps.question.urls")),
    path("api/docs/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path('sentry-debug/', trigger_error),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

# Admin customization
admin.site.site_header = "Vibes Only Django Administration Panel"
admin.site.index_title = "Vibes Only"
admin.site.site_title = "Vibes Only Django Admin"
