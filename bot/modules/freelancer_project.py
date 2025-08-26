from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNEL_ID

router = Router()


class Form(StatesGroup):
    selecting_action = State()
    receiving_input = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Starts the conversation and shows the main menu."""
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="I am a freelancer", callback_data="freelancer"
        ),
        types.InlineKeyboardButton(text="I have a project", callback_data="project"),
    )
    builder.adjust(2)
    await message.reply(
        "Hi! Welcome. Please select an option:", reply_markup=builder.as_markup()
    )
    await state.set_state(Form.selecting_action)


@router.callback_query(Form.selecting_action, F.data == "freelancer")
async def freelancer_handler(callback: CallbackQuery, state: FSMContext):
    """Asks the freelancer to provide their resume and stores the choice."""
    await callback.answer()
    await state.update_data(choice="freelancer")
    await callback.message.edit_text("Please write your resume now:")
    await state.set_state(Form.receiving_input)


@router.callback_query(Form.selecting_action, F.data == "project")
async def project_handler(callback: CallbackQuery, state: FSMContext):
    """Asks the user to provide details about their project and stores the choice."""
    await callback.answer()
    await state.update_data(choice="project")
    await callback.message.edit_text("Please describe your project now:")
    await state.set_state(Form.receiving_input)


@router.message(Form.receiving_input)
async def receive_input(message: Message, state: FSMContext):
    """Receives the user's input, adds user info and a hashtag, and sends it to the channel."""
    bot = message.bot
    user_input = message.text
    user = message.from_user
    data = await state.get_data()
    choice = data.get("choice")

    user_info = f"<b>User:</b> <a href='tg://user?id={user.id}'>{user.full_name}</a>\n"
    if user.username:
        user_info += f"<b>Username:</b> @{user.username}\n"
    if choice == "freelancer":
        final_message = (
            f"<b>New Freelancer!</b>\n\n{user_info}\n{user_input}\n\n#freelancer"
        )
    elif choice == "project":
        final_message = f"<b>New Project!</b>\n\n{user_info}\n{user_input}\n\n#project"
    else:
        final_message = user_input
    await bot.send_message(
        chat_id=CHANNEL_ID, text=final_message, disable_web_page_preview=True
    )
    await message.reply(
        "Your message has been sent to the @moonlancers channel. Thank you!"
    )
    await state.clear()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    """Cancels and ends the conversation."""
    await message.reply("The process has been canceled.")
    await state.clear()
