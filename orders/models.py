from django.db import models

class Order(models.Model):
    first_name = models.CharField(max_length=200,default='unknown')
    last_name = models.CharField(max_length=200,default='unknown')
    email = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "order with the id" + str(self.id)

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name
    @classmethod
    def fields(self):
        return ['id','first_name','email']



class OrderItem(models.Model):
    product_title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "order item for " + str(self.id)
