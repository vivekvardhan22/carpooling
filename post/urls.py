from django.urls import path
from post.views import index, NewPost,  PostDetails, tags, search_view, search_results

urlpatterns = [
   	path('', index, name='index'),
       path('newpost/', NewPost, name='newpost'),
       path('<uuid:post_id>', PostDetails, name='postdetails'),
       path('tag/<slug:tag_slug>', tags, name='tags'),
       path('search/', search_view, name='search'),
       path('search/results/', search_results, name='search_results'),
]