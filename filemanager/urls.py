from django.urls import path, include
from .views import FileAttachmentView, CommentViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('attachments/', FileAttachmentView.as_view(), name='file-attachment-create'), 
    path('attachments/<int:pk>/', FileAttachmentView.as_view(), name='file-attachment-detail'),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)