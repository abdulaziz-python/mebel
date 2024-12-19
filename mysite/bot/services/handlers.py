from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from .constants import NAME, PHONE, FURNITURE_ID
from .conversation import handle_order_creation, handle_start

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_start(update, context)

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ismingizni kiriting:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("Mebel ID raqamini kiriting (4 ta raqam):")
    return FURNITURE_ID

async def get_furniture_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    success = await handle_order_creation(update, context, update.message.text)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Buyurtma bekor qilindi.")
    return ConversationHandler.END

