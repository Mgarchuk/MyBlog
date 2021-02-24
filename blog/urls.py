from django.conf.urls import url
from django.urls import path
from django.views.generic import ListView
from blog.models import Post
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/', ListView.as_view(queryset=Post.objects.all().order_by("-published_date"), template_name='blog/post_list.html')),
    path('edit_post/', views.edit_post, name='post_edit'),
    path('entry/', views.MyProjectLoginView.as_view(), name='entry_page'),
    path('register/', views.RegisterUserView, name='register_page'),
    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<int:pk>', views.update_post, name='update_post'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('create_photo/', views.create_photo, name='create_photo'),
    path('logout/', views.MyProjectLogout.as_view(), name='logout'),
    path('photo_list/', views.photo_list, name='photo_list'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
