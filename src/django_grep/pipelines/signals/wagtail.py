# from .consumers import MyConsumer
# from channels.layers import get_channel_layer



# from django.contrib.auth.models import Group as DjangoGroup
# from wagtail.users.models import Group as WagtailGroup

# # Signal to create a Wagtail group when a Django group is created
# @receiver(post_save, sender=DjangoGroup)
# def create_wagtail_group(sender, instance, created, **kwargs):
#     if created:  # Only create if it's a new group
#         WagtailGroup.objects.get_or_create(name=instance.name)

# # Signal to create a Django group when a Wagtail group is created
# @receiver(post_save, sender=WagtailGroup)
# def create_django_group(sender, instance, created, **kwargs):
#     if created:  # Only create if it's a new group
#         DjangoGroup.objects.get_or_create(name=instance.name)

# # @receiver(post_save, sender=YourModel)  # Replace 'YourModel'
# def model_changed(sender, instance, created, **kwargs):
#     channel_layer = get_channel_layer()
#     group_name = f'model_{instance.pk}'  # Use model ID for group name
#     async def send_update():
#         await channel_layer.group_send(
#             group_name,
#             {
#                 'type': 'model_update',
#                 'data': {
#                     'id': instance.pk,
#                     'field': 'your_field',  # The field that changed
#                     'value': getattr(instance, 'your_field'),
#                 }
#             }
#         )
#     asyncio.run(send_update())
