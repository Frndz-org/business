from ninja import Router
from directory.api import router as directory_router
from location.api import router as location_router

router = Router()

router.add_router("", directory_router)
router.add_router("", location_router)
