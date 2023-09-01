from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/<str:username>/', views.user_blog, name='user-blog'),
    path('myblog/', views.my_blog, name='my-blog'),
    path('friends/', views.friends, name='friends'),
    path('post/<slug:post_slug>/', views.post, name='post'),
    path('category/<slug:category_slug>/', views.posts_by_category, name='by_category'),
    path('tag/<slug:tag_slug>', views.posts_by_tag, name='by_tag'),
    path('create-post/', views.create_post, name='create-post'),
    path('update-post/<str:pk>', views.update_post, name='update-post'),
    path('delete-post/<str:pk>', views.delete_post, name='delete-post'),
    path('like/<int:post_id>', views.like_post, name='like_post'),
    path('bookmark/<int:post_id>', views.bookmark_post, name='bookmark_post'),
    path('bookmarks/', views.user_bookmarks, name='user_bookmarks')
]
