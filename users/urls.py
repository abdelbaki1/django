from django.urls import path
from .views import (
    register, login, logout, AuthenticatedUser, PermissionAPIView, RoleViewSet,
    ProfileInfoAPIView, ProfilePasswordAPIView, listroleview, UserAPIView, UserlistAPI,
    UserActivityView , unpagenatedroleview
)

urlpatterns = [
    path('register', register),
    path('login', login, name="login_view"),
    path('logout', logout),
    path('user', AuthenticatedUser.as_view()),
    path('users/<int:pk>', UserAPIView.as_view()),
    path('users/create', UserAPIView.as_view()),
    path('users/info', ProfileInfoAPIView.as_view()),
    path('users/password', ProfilePasswordAPIView.as_view()),
    path('users', UserlistAPI.as_view()),
    path('permissions', PermissionAPIView.as_view()),
    path('roles', listroleview.as_view()),
    path('unpagenatedroles', unpagenatedroleview.as_view()),
    path('roles/create', RoleViewSet.as_view()),
    path('roles/<str:pk>', RoleViewSet.as_view()),
    path('log', UserActivityView.as_view())]
# path('users', UserGenericAPIView.as_view()),
