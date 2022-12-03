from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, GenericAPIView, UpdateAPIView, CreateAPIView
from rest_framework.generics import DestroyAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from testproject.pagination import CustomPagination
from .auth import generate_access_token, JWTAuthentication
from .models import User, Permission, Role, token, User_activity
from .Signals import user_activity_signal
from .auth import JWTAuthentication
from django.contrib.auth.models import Group,Permission
from .serializers import UserSerializer, PermissionSerializer, RoleSerializer,User_activity_serializer



@api_view(['POST'])
def register(request):
    data = request.data
    print(data)
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match!')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    group_name : str = request.data.get('group_name')
    group_instance = Group.objects.get(name=group_name.lower())
    user_instance  = serializer.save()
    user_instance.groups.add(group_instance)
    user_activity_signal.send(sender=user_instance,activity=' just registered')
    user_instance.save()
    # print(user_instance.groups)
    return Response(serializer.data)


@api_view(['POST'])
def login(request):

    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect Password!')
    response = Response()
    user.user_permissions.set(user.groups.all()[0].permissions.all())
    # print(user,user.groups.get(name='patient').permissions.all())
    token = generate_access_token(user)
    res=user_activity_signal.send(sender=user, activity='have logged in !!')
    response.set_cookie(key='jwt', value=token, httponly=True, samesite='none', secure=True)
    response.data = {
        'jwt': token,
        'type':user.groups.all()[0].name
    }
    return response


@api_view(['POST'])
# @login_required(redirect_field_name='login_view')
def logout(request):
    response = Response()
    t=request.COOKIES.get('jwt')
    response.delete_cookie(key='jwt')
    request.user=JWTAuthentication().authenticate(request)[0]
    if(request.user):
        user_activity_signal.send(sender=request.user, activity='have logged out from his account')
    


    response.data = {
        'message': 'Success'
    }
    # user_activity_signal.send(sender=,activity='user has just logout frm the system')
    return response


class AuthenticatedUser(APIView):
    '''return the current user along with it's permission'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserSerializer(request.user).data
        print(data)
        user:User =request.user
        user.user_permissions.set(request.user.groups.all()[0].permissions.all())
        user.save()
        data['type_name'] = request.user.groups.all()[0].name
        return Response(data)


class PermissionAPIView(ListAPIView):
    '''
    return all the permission in a list
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class genericroleview(GenericAPIView, PermissionRequiredMixin):
    '''
    generic api config for the role model
    '''
    model = 'Role'
    def get_permission_required(self):
        if self.request.method == 'GET':
            return ['view_'+ self.model.lower()]
        if self.request.method == 'POST':
            return ['add_'+ self.model.lower()]
        if self.request.method == 'DELETE':
            return ['delete_'+ self.model.lower()]
        if self.request.method == 'PUT':
            return ['change_'+ self.model.lower()]

    def has_permission(self):
        return all(
            self.request.user.user_permissions.filter(codename=i).exists() for i in self.get_permission_required()
            )
    def get_object(self):
        if(self.has_permission()):
            print("user has permission")
            return super().get_object()
        else:
            print("no permission granted")
            raise PermissionDenied("good luck next time")
    # permission_required = ('change_role','add_role','delete_role')
    
    authentication_classes = [JWTAuthentication]
    serializer_class = RoleSerializer
    queryset = Group.objects.all().order_by('name')

class unpagenatedroleview(genericroleview,ListAPIView):
     pass
class listroleview(genericroleview, ListAPIView):
    '''
    return list of role
    '''
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']


class RoleViewSet(genericroleview, RetrieveUpdateDestroyAPIView, CreateAPIView):
    '''return a role,create,update,delete'''

    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "pk"
    permission_required = ('change_role','delete_role','add_role')


    def post(self, request, *args, **kwargs):
        user_activity_signal.send(sender=request.user, activity='have created a role')
        if(self.has_permission()):
            # print("******",request.user.user_permissions.all())
            return self.create(request, *args, **kwargs)
        else :
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        user_activity_signal.send(sender=request.user, activity='have updated a role')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user_activity_signal.send(sender=request.user,activity='have deleted a role')
        return self.destroy(request, *args, **kwargs)


class UserGenericAPIView(GenericAPIView,PermissionRequiredMixin):
    model = 'User'
    def get_permission_required(self):
        if self.request.method == 'GET':
            return ['view_'+ self.model.lower()]
        if self.request.method == 'POST':
            return ['add_'+ self.model.lower()]
        if self.request.method == 'DELETE':
            return ['delete_'+ self.model.lower()]
        if self.request.method == 'PUT':
            return ['change_'+ self.model.lower()]
    def has_permission(self):
        return all(
            self.request.user.user_permissions.filter(codename=i).exists() for i in self.get_permission_required()
            )
    def get_object(self):
        if(self.has_permission()):
            print("user has permission")
            return super().get_object()
        else:
            print("no permission granted")
            raise PermissionDenied("good luck next time")
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserlistAPI(UserGenericAPIView, ListAPIView):
    '''
    return a list of all users
    '''
    # permission_required = ('view_user','add_user')
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ['first_name']


class UserAPIView(UserGenericAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView):
    '''retrieve ,update,delete create a user'''
    def post(self, request, *args, **kwargs):
        
        user_activity_signal.send(sender=request.user, activity='have created a user')
        if(self.has_permission()):
            return self.create(request, *args, **kwargs)
        else :
            raise PermissionDenied
    
    permission_classes = [IsAuthenticated]
    # permission_required = ('change_user','add_user',)
    
    lookup_field = "id"
    lookup_url_kwarg = 'pk'
    

    def perform_create(self, serializer):
        serializer.save(role_id=self.request.data.get('role_id'))

    def update(self, request, *args, **kwargs):
        # print("update has been hit***********************************")
        # partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = User.objects.get(id=instance.id)
        user.email = request.data.get('email')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        group = Group.objects.get(id=request.data.get('role_id'))
        user.groups.set([group])
        user.save()
        return Response(UserSerializer(user).data)


class ProfileInfoAPIView(UpdateAPIView):
    '''
    updateuserinfo
    '''
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        print("update has been hitttz")
        # partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = User.objects.get(id=instance.id)
        user.email = request.data.get('email')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.user_image=request.data.get('user_image')
        user.save(update_fields=request.data.keys())
        user_activity_signal.send(user,activity='have updated his profile')
        return Response(UserSerializer(user).data)


class ProfilePasswordAPIView(APIView):
    '''
    update the password
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError('Passwords do not match')
        user.set_password(request.data['password'])
        user.save()
        serializer = UserSerializer(user)
        user_activity_signal.send(sender=user,activity='has changed his password')
        return Response(serializer.data)
class UserActivityView(ListAPIView):
    serializer_class = User_activity_serializer
    queryset = User_activity.objects.all().order_by('date')
    pagination_class = CustomPagination
    
