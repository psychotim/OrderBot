from aiogram import Router

from src.routers.client_logic.client import client_router
from src.routers.basic import basic_router
from src.routers.admin_logic.admin import admin_router
from src.routers.client_logic.commands.help import help_router
from src.routers.client_logic.commands.start import start_router

router = Router(name='main')
router.include_routers(
    client_router,
    basic_router,
    admin_router,
    help_router,
    start_router
)
