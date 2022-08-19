from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView

from .views import PostCreateView, PostRetrieveView, LikePostView, UnlikePostView, UsersAnalyticsView, \
    TokenObtainPairView, LikesAnalyticsView


urlpatterns = [
    path('', include('djoser.urls')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('post/create', PostCreateView.as_view()),
    path('post/<int:pk>', PostRetrieveView.as_view()),
    path('post/<int:pk>/like', LikePostView.as_view()),
    path('post/<int:pk>/unlike', UnlikePostView.as_view()),
    path('analitics/me', UsersAnalyticsView.as_view()),
    path('analitics/', LikesAnalyticsView.as_view())
]