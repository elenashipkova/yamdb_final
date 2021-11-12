from django.urls import include, path

from rest_framework import routers

from ..views import CommentViewSet, ReviewViewSet


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/categories/', include('titles.urls.category')),
    path('v1/genres/', include('titles.urls.genre')),
    path('v1/titles/', include('titles.urls.titles')),
    path('v1/', include(router.urls))
]
