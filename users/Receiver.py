# import dispatch
from django.dispatch import receiver
# import the custopm signals
from .Signals import user_activity_signal
# from .models import user_activity

# # create the function and connect it with the receive methode
# # @receiver(signals.user_connected_signal)
# def print_user_connected(sender,activity,**kwargs):
#     user_instance = user_activity.objects.get_or_create(user=sender)
#     user_instance.activity=activity
    
#     user_instance.save()
#     print(**kwargs)
#     print("***************")

# user_connected_signal.connect(print_user_connected,weak=False)