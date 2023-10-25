from django.urls import path,include
from .views import PostList, PostDetails, AuthorList, AuthorDetails,AuthorRegister, AuthorLogin, AuthorLogOut

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("api/posts", PostList.as_view(), name="api_post_list"),
    path("api/posts/<slug:slug>",
         PostDetails.as_view(),
         name="api_post_details"),
    path("api/authors", AuthorList.as_view(), name="api_author_list"),
    path("api/authors/<slug:slug>",
         AuthorDetails.as_view(),
         name="api_author_details"),
    path("api/author/register", AuthorRegister.as_view(), name="api_author_register"),
    path("api/author/login", AuthorLogin.as_view(), name="api_author_login"),
  path("api/author/register", AuthorRegister.as_view(), name="api_author_register"),
    path("api/author/login", AuthorLogin.as_view(), name="api_author_login"),
  path('api/author/logout',AuthorLogOut.as_view(), name='logout'),
  
  
  
]


