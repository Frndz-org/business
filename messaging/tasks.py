import celery.exceptions
import sentry_sdk

from business.celery import app
from business.utils import Utility, broker_publish
from messaging.models import Template


@app.task(bind=True, max_retries=3)
def prepare_notification(self, payload: dict, event: str):
    """
    Responsible for retrieving the appropriate Event notification
    template and replacing placeholders of template message
    """
    try:
        event_template = Template.objects.get(event=event)

        event_template.message = Utility.placeholder_replace(payload=payload, text=event_template.message)

        notification = {
            'email': {
                'recipient': payload['recipient'],
                'body': event_template.message,
                'subject': event_template.subject
            }
        }

        # Publish to the notification service
        broker_publish('new-notification', notification)
    except (Template.DoesNotExist, Template.MultipleObjectsReturned):
        sentry_sdk.capture_message(f"Messaging Template not available for event: {event}", "error")
        pass

    except Exception as ex:
        try:
            sentry_sdk.capture_exception(ex)
            self.retry(countdown=10)
        except celery.exceptions.MaxRetriesExceededError:
            pass
