from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post
from .serializers import PostSerializer

class PostView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  def get(self, request):
    try:
      posts = Post.objects.filter(user = request.user)
      serializer = PostSerializer(posts, many = True)

      return Response({
        'data': serializer.data,
        'message': 'Posts fetched success'
      }, status=status.HTTP_200_OK)
    
    except Exception as e:
      print(e)
      return Response({
        'data' : {},
        'message' : 'Something went wrong'
      }, status=status.HTTP_400_BAD_REQUEST)

  def post(self, request):
    try:
      data = request.data
      data['user'] = request.user.id
      serializer = PostSerializer(data = data)

      if not serializer.is_valid():
        print(serializer.errors)
        return Response({
          'data': serializer.errors,
          'message': 'Something went wrong'
        }, status=status.HTTP_400_BAD_REQUEST)
      
      serializer.save()

      return Response({
        'data': serializer.data,
        'message': 'Post created success'
      }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
      print(e)
      return Response({
        'data' : {},
        'message' : 'Something went wrong'
      }, status=status.HTTP_400_BAD_REQUEST)

