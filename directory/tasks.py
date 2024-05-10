from business.celery import app
from directory.models import Profile


@app.task(bind=True, max_retries=3)
def get_business_info(self, profile_id: int):
    """

    :param self:
    :param profile_id:
    :return:
    """
    try:

        profile = Profile.objects.get(pk=profile_id)

        return {'business_name': profile.name, 'tax_id': profile.tax_id}

    except Profile.DoesNotExist:
        pass
