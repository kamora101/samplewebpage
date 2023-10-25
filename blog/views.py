from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .validations import registeration_validation

from rest_framework import status, generics, permissions
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model, login, logout
from .paginations import PageNumberPagination




from .models import Post, Author
from .forms import PostForm
from .serializers import PostSerializer, AuthorSerializer, AuthorRegisterSerializer, AuthorLoginSerializer 
from .permissions import IsAuthorOrReadOnly
from .validations import registeration_validation, validate_email, validate_password


#API Views

class PostList(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  pagination_class = PageNumberPagination
  filterset_fields=['author','status', 'created_on']
  def perform_create(self, serializer):
    serializer.save(author=self.request.user.blog_author)

class PostDetails(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

  lookup_field = 'slug'


class AuthorList(generics.ListCreateAPIView):
  queryset = Author.objects.all()
  serializer_class = AuthorSerializer

class AuthorDetails(generics.RetrieveUpdateDestroyAPIView):
  queryset = Author.objects.all()
  serializer_class = AuthorSerializer
  lookup_field = 'slug'


class AuthorRegister(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        clean_data = registeration_validation(request.data)
        serializer = AuthorRegisterSerializer(data=clean_data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
              serializer = AuthorRegisterSerializer(user, context={'request': request})
              return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AuthorLogin(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = (SessionAuthentication, )

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
      
        serializer = AuthorLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
          user = serializer.check_author(data)
          login(request, user)
          serializer = AuthorLoginSerializer(user, context={'request': request})
          return Response(serializer.data, status=status.HTTP_200_OK)



class AuthorLogOut(APIView):
  permission_classes=(permissions.AllowAny, )
  authentication_classes=()
  def post (self, request):
    logout(request)
    return Response (status=status.HTTP_200_OK)



