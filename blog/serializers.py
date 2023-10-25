from rest_framework import serializers
from django.contrib.sessions.models import Session
from .models import Post
from django.contrib.auth import get_user_model, authenticate

AuthorModel = get_user_model()


class PostSerializer(serializers.ModelSerializer):
  author=serializers.ReadOnlyField(source='author.name')
  class Meta:
    model=Post
    fields='__all__'

class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = AuthorModel
    fields = ['email', 'name', 'slug', 'bio', 'avatar']
    lookup_field='slug'



class AuthorRegisterSerializer(serializers.ModelSerializer):
    session_key = serializers.SerializerMethodField(read_only=True)
    author_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AuthorModel
        fields = ['session_key', 'author_details']

    def create(self, clean_data):
        email = clean_data.pop('email')
        password = clean_data.pop('password')
        print(clean_data)
        author_obj = AuthorModel.objects.create_user(email=email,
                                                     password=password,
                                                     **clean_data)
        author_obj.username = email
        author_obj.save()
        return author_obj

    def get_session_key(self, obj):
        # Retrieve session key for the logged-in user
        session = Session.objects.filter(
            session_key=self.context['request'].session.session_key).first()
        return session.session_key if session else None

    def get_author_details(self, obj):
        # Use the AuthorSerializer to serialize the authenticated author
        return AuthorSerializer(obj).data


class AuthorLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    session_key = serializers.SerializerMethodField(read_only=True)
    author_details = serializers.SerializerMethodField(
        read_only=True)  # Add this line to include the serialized author

    def get_session_key(self, obj):
        # Retrieve session key for the logged-in user
        session = Session.objects.filter(
            session_key=self.context['request'].session.session_key).first()
        return session.session_key if session else None

    def get_author_details(self, obj):
        # Use the AuthorSerializer to serialize the authenticated author
        return AuthorSerializer(obj).data

    def check_author(self, clean_data):
        author = authenticate(username=clean_data['email'],
                              password=clean_data['password'])
        if not author:
            raise serializers.ValidationError('Error: Author not found!')
        return author
