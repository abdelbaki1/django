from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from testproject.pagination import CustomPagination
from products.models import Product
from products.serializers import ProductSerializer
from users.auth import JWTAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.filters import SearchFilter
from django.core.exceptions import PermissionDenied
from users.Signals import user_activity_signal
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission



class GenericProductView(GenericAPIView,PermissionRequiredMixin):
    model :str = "Product"
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Product.objects.all().order_by('title')
    serializer_class = ProductSerializer
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
        print(self.get_permission_required(),self.request.user.user_permissions.all())
        if(self.has_permission()):
            print("user has permission")
            return super().get_object()
        else:
            print("no permission granted")
            raise PermissionDenied("good luck next time")


class getallproduct(GenericProductView, ListModelMixin):
    permission_required = ('view_product')
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    search_fields = ['title']
    filter_backends = [SearchFilter]

    def get(self, request, *args, **kwargs):
        print('view_'+ self.get_queryset().__class__.__name__)
        return self.list(request,
                         *args,
                         **kwargs)


class productapi(GenericProductView,
                 CreateModelMixin,
                 UpdateModelMixin,
                 RetrieveModelMixin,
                 DestroyModelMixin,
                ):
    permission_required = ('view_product','add_product','delete_product')
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if(self.has_permission()):
            user_activity_signal.send(sender=self.request.user,activity='have created a product')
            return self.create(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        user_activity_signal.send(sender=self.request.user,activity='have updated a product')
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        print(request.user.user_permissions.all())
        user_activity_signal.send(sender=self.request.user,activity='have deleted a product')
        return self.destroy(request, *args, **kwargs)
