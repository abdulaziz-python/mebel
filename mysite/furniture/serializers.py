from rest_framework import serializers
from .models import Furniture, FurnitureImage

class FurnitureImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnitureImage
        fields = ('id', 'image')

class FurnitureSerializer(serializers.ModelSerializer):
    images = FurnitureImageSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Furniture
        fields = ('furniture_id', 'name', 'description', 'price', 'video_link', 'images', 'category', 'category_display')

