from django.urls import path, include

from rest_framework import routers

from .views import APIRegEmail, APIRegUser, UserMeViewSet

router = routers.DefaultRouter()
router.register('users', UserMeViewSet, basename='userme')

usersurlpatterns = [
    path('auth/mail/', APIRegEmail.as_view(), name='reg_email'),
    path('auth/token/', APIRegUser.as_view(), name='reg_user'),
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(usersurlpatterns)),
]
