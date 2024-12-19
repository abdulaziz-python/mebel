"""Admin notification service for the bot."""
from telegram import Bot
from django.conf import settings
from typing import List

async def notify_admins(bot: Bot, message: str) -> None:

    admin_usernames: List[str] = settings.ADMIN_TELEGRAM_IDS
    
    for admin in admin_usernames:
        try:
            await bot.send_message(chat_id=admin, text=message)
        except Exception as e:
            print(f"Error sending message to admin {admin}: {e}")

def format_order_message(order) -> str:

    return (
        f"🆕 Yangi buyurtma!\n\n"
        f"👤 Mijoz: {order.customer_name}\n"
        f"📞 Tel: {order.phone_number}\n"
        f"🛋 Mebel: {order.furniture.name}\n"
        f"🔢 Mebel ID: {order.furniture.furniture_id}\n"
        f"💰 Narxi: {order.furniture.price:,} UZS"
    )