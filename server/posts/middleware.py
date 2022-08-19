from django.utils.deprecation import MiddlewareMixin

from .helpers import set_activity
from .helpers import get_user_by_jwt


class ActivityMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = get_user_by_jwt(request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1])
        if user:
            set_activity(user.username)
