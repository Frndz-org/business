from ninja import Router
from directory.api import router as directory_router

router = Router()

router.add_router("", directory_router)
