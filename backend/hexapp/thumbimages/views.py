from .models import ThumbImage, ImageLink
from .serializers import ThumbImageSerializer, ImageLinkListSerializer, ThumbImageSerializer, ImageLinkSerializer, ThumbImageListSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .permissions import IsStaff, IsOwner, CanSee, ExpiredObjectSuperuserOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, renderers, mixins
from django.http import HttpResponseRedirect, FileResponse


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class PassthroughRenderer(renderers.BaseRenderer):
    media_type = ''
    format = ''
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class ImageLinkListViewSet(mixins.ListModelMixin,mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsStaff | IsOwner, CanSee]
    queryset = ImageLink.objects.all()
    serializer_class = ImageLinkListSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return ImageLink.objects.all()
        else:
            return ImageLink.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ImageLinkViewSet(mixins.RetrieveModelMixin,  viewsets.GenericViewSet):
    queryset = ImageLink.objects.all()
    serializer_class = ImageLinkSerializer
    permission_classes = [ExpiredObjectSuperuserOnly]

    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, *args, **kwargs):
        instance = self.get_object()
        print(instance.image)
        file_handle = instance.image.image.open()
        response = FileResponse(file_handle, content_type='whatever')
        response['Content-Length'] = instance.image.image.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.image.image.name
        return response


class ThumbImageViewSet(viewsets.ModelViewSet):
    queryset = ThumbImage.objects.all()
    serializer_class = ThumbImageSerializer
    serializer_classes = {
        'list': ThumbImageListSerializer,
        'retrieve': ThumbImageSerializer,
    }
    default_serializer_class = ThumbImageSerializer
    permission_classes = [IsStaff | IsOwner]
    
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        if self.request.user.is_staff:
            return ThumbImage.objects.all()
        else:
            return ThumbImage.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super(ThumbImageViewSet, self).create(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to='/thumbimages')

    def update(self, request, *args, **kwargs):
        return Response("Succes")
