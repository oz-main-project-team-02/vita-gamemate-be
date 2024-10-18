from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # openapi
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # apps
    path("api/v1/users/", include("users.urls")),
    path("api/v1/wallets/", include("wallets.urls")),
    path("api/v1/games/", include("games.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
    path("api/v1/mates/", include("mates.urls")),
]
