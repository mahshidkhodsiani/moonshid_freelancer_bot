import logging

from aiogram import Router

router = Router()


@router.message.middleware()
async def log_message(handler, event, data):
    """Log all incoming messages."""
    user = event.from_user
    logging.info(f"Message from {user.full_name} (ID: {user.id}): {event.text}")
    return await handler(event, data)


@router.callback_query.middleware()
async def log_callback(handler, event, data):
    """Log all callback queries."""
    user = event.from_user
    logging.info(f"Callback from {user.full_name} (ID: {user.id}): {event.data}")
    return await handler(event, data)
