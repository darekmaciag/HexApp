from rest_framework import serializers
from .models import ThumbImage,ImageLink
from django.contrib.auth.models import User


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     thumbimages = serializers.HyperlinkedRelatedField(many=True, view_name='thumbimage-detail', read_only=True)

#     class Meta:
#         model = User
#         fields = ['url', 'id', 'username', 'thumbimages']


class ImageLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageLink
        fields = ['url']


class ImageLinkListSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = ImageLink
        fields = ['url', 'owner', 'expiry_time', 'image']

    def __init__(self, *args, **kwargs):
        super(ImageLinkListSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        if request_user.is_superuser:
            self.fields['image'].queryset = ThumbImage.objects.all()
        else:    
            self.fields['image'].queryset = ThumbImage.objects.filter(owner=request_user)


class ThumbImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbImage
        fields = ['url']

        
class ThumbImageSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    links = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='thumbimage-detail')

    class Meta:
        model = ThumbImage
        fields = fields = ['id', 'owner', 'created', 'title', 'alt', 'image', 'image_small', 'image_medium', 'links']

    def to_representation(self,instance):
        ret = super(ThumbImageSerializer,self).to_representation(instance)
        image = ['image']
        image_large = ['image_medium']
        image_medium = ['links']
        if self.context['request'].user.has_perm('thumbimages.hide_image') and not self.context['request'].user.is_superuser:
            [ret.pop(field,'') for field in image]
        if self.context['request'].user.has_perm('thumbimages.hide_image_medium') and not self.context['request'].user.is_superuser:
            [ret.pop(field,'') for field in image_large]
        if self.context['request'].user.has_perm('thumbimages.hide_image_link') and not self.context['request'].user.is_superuser:
            [ret.pop(field,'') for field in image_medium]
        return ret

