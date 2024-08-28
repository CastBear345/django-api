from .models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    exclude = ['created_at', 'updated_at']