from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Send a help message when the command /help is issued."""
    await message.reply(
        "MoonshidBot - A modular Telegram bot for connecting freelancers and project owners.\n\n"
        "Use /start to begin the conversation.\n"
        "Use /help for this message."
    )
