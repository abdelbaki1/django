from rest_framework import serializers
from products.models import Product
from .models import OrderItem, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    # product_title=ProductSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'
        # exclude = ['order']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)
    total = serializers.SerializerMethodField('get_total')

    def get_total(self, obj):
        items = OrderItem.objects.all().filter(order_id=obj.id)
        return sum((o.price * o.quantity) for o in items)

    class Meta:
        model = Order
        fields = '__all__'
    def create(self,validated_data):
        # create the order object
        order_object = Order.objects.create(**validated_data)
        order_object.save()
        print(order_object)
        # loop through all the order items and add them to the order object
        if('order_items' in validated_data.keys()):
            orders_items = validated_data.pop('order_items')
            for order_item in orders_items:
                print(dict(order_item))
                order_item_object = OrderItem.objects.create(**dict(order_item))
                print(order_item_object.order)
                order_item_object.order = order_object
                order_item_object.save()
        return order_object
        # return order object
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get('email',instance.email)

        for order_item in validated_data.get('order_items'):
            OrderItem.objects.filter(order__id=instance.id).update(**dict(order_item))
        return instance
