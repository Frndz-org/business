from celery import chain
from django.db.models.signals import post_save
from django.dispatch import receiver

from business.utils import broker_publish
from directory.models import Profile
from directory.tasks import get_business_info
from messaging.models import Event

from messaging.tasks import prepare_notification


@receiver(post_save, sender=Profile)
async def on_profile_save(sender, instance, created, **kwargs):
    """

    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """

    if created:
        stream_data = {'user_id': instance.owner.__str__()}
        broker_publish('user_info', stream_data)
        chain(get_business_info.s(profile_id=instance.pk), prepare_notification.s(event=Event.Nb)).apply_async(
            countdown=2)
