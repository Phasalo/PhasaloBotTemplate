from .admin import router as admin_router
from .default import router as default_router
from .inline import router as inline_router
from .phasalo_drollery import router as phasalo_drollery_router

__all__ = [
    'admin_router',
    'default_router',
    'inline_router',
    'phasalo_drollery_router',
]
