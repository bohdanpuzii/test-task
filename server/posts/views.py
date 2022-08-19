import datetime

from rest_framework.generics import GenericAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from drf_spectacular.utils import extend_schema

from .serializers import PostCreateSerializer, PostRetrieveSerializer, LikePostSerializer, MyTokenObtainPairSerializer
from .models import Post, PostLikes
from .helpers import get_activity, get_like_stats_by_days, check_and_convert_date_to_object
from .swagger_examples import LikeActivityQueryParamsExample


class PostCreateView(GenericAPIView):
    serializer_class = PostCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response('Not valid data', status=400)


class PostRetrieveView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer


class LikePostView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = LikePostSerializer

    def perform_create(self, serializer):
        post = self.get_object()
        return serializer.save(post=post)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            'status': 201,
            'message': 'Liked',
            'likes_count': PostLikes.objects.filter(post=self.get_object()).count(),
        })


class UnlikePostView(DestroyAPIView):
    queryset = Post.objects.all()

    def check_permissions(self, request):
        if not PostLikes.objects.filter(post=self.get_object(), user=request.user).exists():
            self.permission_denied(
                request, message='Not liked yet'
            )

    def perform_destroy(self, instance):
        return PostLikes.objects.filter(user=self.request.user, post=instance).delete()

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            'status': 204,
            'message': 'Unliked',
            'likes_count': PostLikes.objects.filter(post=self.get_object()).count(),
        })


class UsersAnalyticsView(GenericAPIView):

    def get(self, request):
        response_body = {'last_activity': get_activity(request.user.username), 'last_login': request.user.last_login}
        return Response(response_body)


class TokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super(TokenObtainPairView, self).post(request, args, kwargs)
        return response


class LikesAnalyticsView(GenericAPIView):

    def process_query_params(self):
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        date_from = check_and_convert_date_to_object(self.request.query_params.get('date_from')) if date_from \
            else (datetime.datetime.today() - datetime.timedelta(days=14)).date()
        date_to = check_and_convert_date_to_object(self.request.query_params.get('date_to')) if date_to \
            else datetime.datetime.today()
        return date_from, date_to

    def get_queryset(self):
        user = self.request.user
        date_from, date_to = self.process_query_params()
        queryset = PostLikes.objects.filter(date_created__gte=date_from, date_created__lte=date_to, user=user)
        return queryset

    @extend_schema(parameters=LikeActivityQueryParamsExample)
    def get(self, request, *args, **kwargs):
        likes = self.get_queryset()
        date_from, date_to = self.process_query_params()
        response = get_like_stats_by_days(date_from, date_to, likes)
        return Response(response)
