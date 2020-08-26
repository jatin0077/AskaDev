from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('<slug:uname>', views.UserProfileView.as_view(), name='profile'),
    path('<int:pk>/edit-profile/', views.UserProfileUpdateView.as_view(), name='edit_profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)