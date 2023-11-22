from aiogram import Router

from src.routers.client import client_router
from src.routers.basic import basic_router
from src.routers.admin import admin_router

router = Router(name='main')
router.include_routers(
    client_router,
    basic_router,
    admin_router
)
