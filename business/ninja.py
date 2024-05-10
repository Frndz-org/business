from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from ninja import Swagger, Redoc, NinjaAPI

from .utils import TokenBasedAuthorization

from .v1 import router as v1_routers

api = NinjaAPI(title="Business Service",
               description="A microservice responsible for handling information on business",
               docs_decorator=staff_member_required,
               docs=Redoc() if not settings.DEBUG else Swagger(),
               auth=TokenBasedAuthorization()
               )

api.add_router("/v1/", v1_routers)
