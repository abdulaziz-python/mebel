from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from furniture.models import Furniture, Order
from .admin_notification import notify_admins, format_order_message
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.conf import settings

@sync_to_async
def get_furniture(furniture_id):
    try:
        return Furniture.objects.get(furniture_id=furniture_id)
    except ObjectDoesNotExist:
        return None

@sync_to_async
def create_order(furniture, customer_name, phone_number):
    return Order.objects.create(
        furniture=furniture,
        customer_name=customer_name,
        phone_number=phone_number
    )

def format_admin_message(order):
    admin_url = settings.SITE_URL + reverse('admin:furniture_order_change', args=[order.id])
    return (
        f"🆕 Yangi mebel buyurtmasi!\n\n"
        f"👤 Mijoz: {order.customer_name}\n"
        f"📞 Tel: {order.phone_number}\n"
        f"🛋 Mebel: {order.furniture.name}\n"
        f"🔢 Mebel ID: {order.furniture.furniture_id}\n"
        f"💰 Narxi: {order.furniture.price:,} UZS\n\n"
        f"📊 Admin panel: {admin_url}"
    )

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🛋 Buyurtma berish")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Assalomu alaykum! Mebel do'konimizga xush kelibsiz!\n"
        "Buyurtma berish uchun '🛋 Buyurtma berish' tugmasini bosing.",
        reply_markup=reply_markup
    )

async def handle_order_creation(update: Update, context: ContextTypes.DEFAULT_TYPE, furniture_id: str):
    furniture = await get_furniture(furniture_id)
    if furniture is None:
        await update.message.reply_text(
            "Kechirasiz, bunday ID raqamli mebel topilmadi.\n"
            "Iltimos, qaytadan urinib ko'ring."
        )
        return False

    order = await create_order(
        furniture,
        context.user_data['name'],
        context.user_data['phone']
    )
    
    admin_message = format_admin_message(order)
    await notify_admins(context.bot, admin_message)
    
    await update.message.reply_text(
        "Buyurtmangiz qabul qilindi! ✅\n"
        "Tez orada operatorlarimiz siz bilan bog'lanishadi."
    )
    return True

