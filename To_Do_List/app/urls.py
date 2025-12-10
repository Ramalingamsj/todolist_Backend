from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ListViewset, SignupApiView, LoginAPIView

router = DefaultRouter()
router.register("list", ListViewset, basename="list")

urlpatterns = [
    path("signup/", SignupApiView.as_view(), name="user-signup"),
    path("login/", LoginAPIView.as_view(), name="user-login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
