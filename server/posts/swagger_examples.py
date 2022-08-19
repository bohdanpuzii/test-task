from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

LikeActivityQueryParamsExample = [
            OpenApiParameter("date_from", OpenApiTypes.STR, OpenApiParameter.QUERY, examples=[OpenApiExample(
                'example_date', '2020-02-02')]),
            OpenApiParameter("date_to", OpenApiTypes.STR, OpenApiParameter.QUERY, examples=[OpenApiExample(
                'example_date', '2020-02-15')])
        ]
