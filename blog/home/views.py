from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post
from .serializers import PostSerializer

from django.db.models import Q
from django.core.paginator import Paginator

class PublicPost(APIView):
  def get(self, request):
    try:
      posts = Post.objects.all().order_by('?')

      if request.GET.get('search'):
        search = request.GET.get('search')
        posts = posts.filter(Q(title__icontains = search) | Q(post_text__icontains = search))

      page_number = request.GET.get('page', 1)
      paginator = Paginator(posts, 10)

      serializer = PostSerializer(paginator.page(page_number), many = True)

      return Response({
        'data': serializer.data,
        'message': 'Posts fetched success'
      }, status=status.HTTP_200_OK)
    
    except Exception as e:
      print(e)
      return Response({
        'data' : {},
        'message' : 'Something went wrong or invalid page'
      }, status=status.HTTP_400_BAD_REQUEST)

class PostView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  def get(self, request):
    try:
      posts = Post.objects.filter(user = request.user)

      if request.GET.get('search'):
        search = request.GET.get('search')
        posts = posts.filter(Q(title__icontains = search) | Q(post_text__icontains = search))

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

  def patch(self, request):
    try:
      data = request.data

      post = Post.objects.filter(uid = data.get('uid'))

      if not post.exists():
        return Response({
          'data' : {},
          'message' : 'Invalid post uid'
        }, status=status.HTTP_400_BAD_REQUEST)

      if request.user != post[0].user:
        return Response({
          'data' : {},
          'message' : 'You are not authorized to this'
        }, status=status.HTTP_400_BAD_REQUEST)

      serializer = PostSerializer(post[0], data = data, partial = True)

      if not serializer.is_valid():
        print(serializer.errors)
        return Response({
          'data': serializer.errors,
          'message': 'Something went wrong'
        }, status=status.HTTP_400_BAD_REQUEST)
      
      serializer.save()

      return Response({
        'data': serializer.data,
        'message': 'Post updated success'
      }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
      print(e)
      return Response({
        'data' : {},
        'message' : 'Something went wrong'
      }, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request):
    try:
      data = request.data

      post = Post.objects.filter(uid = data.get('uid'))

      if not post.exists():
        return Response({
          'data' : {},
          'message' : 'Invalid post uid'
        }, status=status.HTTP_400_BAD_REQUEST)

      if request.user != post[0].user:
        return Response({
          'data' : {},
          'message' : 'You are not authorized to this'
        }, status=status.HTTP_400_BAD_REQUEST)

      post[0].delete()
      
      return Response({
        'data': {},
        'message': 'Post deleted success'
      }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
      print(e)
      return Response({
        'data' : {},
        'message' : 'Something went wrong'
      }, status=status.HTTP_400_BAD_REQUEST)