from aiogram import Router

from src.handlers.client import client_router
from src.handlers.basic import basic_router
from src.handlers.admin import admin_router

router = Router(name='main')
router.include_routers(
    client_router,
    basic_router,
    admin_router
)
