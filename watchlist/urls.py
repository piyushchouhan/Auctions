from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('watchlist', views.watchlist, name='watchlist'),
    path('listing/<int:listing_id>/add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('check_watchlist/', views.check_watchlist, name='check_watchlist'),
    path('remove_from_watchlist/<int:listing_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)