"""Root API router."""

from fastapi import APIRouter

from . import appointments, auth, automations, clients, conversations, services

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(automations.router, prefix="/automations", tags=["automations"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
