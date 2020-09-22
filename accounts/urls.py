from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('<slug:uname>', views.UserProfileView.as_view(), name='profile'),
    path('<uuid:uid>/edit-profile/', views.UserProfileUpdateView.as_view(), name='edit_profile'),
    path('follow/<slug:user>', login_required(views.followUser), name='follow'),
    path('unfollow/<slug:user>', login_required(views.unfollowUser), name='unfollow'),
	path('trending/developers/', views.TopDevelopers.as_view(), name='top_dev'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)