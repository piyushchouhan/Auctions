from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("listing", views.all_listing, name="listing"),
    path("listing/<int:listing_id>/", views.listing, name="listing_detail"),
    path('listing/<int:listing_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('listing/<int:listing_id>/edit_comment/<int:comment_id>/', views.editComment, name='edit_comment'),
    path('listing/delete_listing/<int:listing_id>', views.delete_listing, name='delete_listing'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)