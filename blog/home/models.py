from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

import uuid

class BaseModel(models.Model):
  uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now_add=True)

  class Meta:
    abstract = True

class Post(BaseModel):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
  title = models.CharField(max_length=500)
  post_text = models.TextField()

  def __str__(self) -> str:
    return self.title