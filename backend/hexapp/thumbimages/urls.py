from django.urls import path, include
from rest_framework.routers import DefaultRouter
from thumbimages import views
from django.conf.urls.static import static
from django.conf import settings
from .views import ThumbImageViewSet, ImageLinkViewSet, ImageLinkListViewSet


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'images', views.ThumbImageViewSet)
router.register(r'createlink', views.ImageLinkViewSet)
router.register(r'createlink', views.ImageLinkListViewSet)


urlpatterns = [
    path('', include(router.urls)),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]