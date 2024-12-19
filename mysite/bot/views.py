"""Bot views for handling Telegram webhook and running the bot."""
import asyncio
from django.http import HttpResponse
from django.views import View
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.services.conversation import handle_start, handle_order_creation
import logging
from django.conf import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

NAME, PHONE, FURNITURE_ID = range(3)

class BotView(View):
    async def order_start(self, update, context):
        await update.message.reply_text("Ismingizni kiriting:")
        return NAME

    async def get_name(self, update, context):
        context.user_data['name'] = update.message.text
        await update.message.reply_text("Telefon raqamingizni kiriting:")
        return PHONE

    async def get_phone(self, update, context):
        context.user_data['phone'] = update.message.text
        await update.message.reply_text("Mebel ID raqamini kiriting (4 ta raqam):")
        return FURNITURE_ID

    async def get_furniture_id(self, update, context):
        success = await handle_order_creation(update, context, update.message.text)
        return ConversationHandler.END

    async def cancel(self, update, context):
        await update.message.reply_text("Buyurtma bekor qilindi.")
        return ConversationHandler.END

    def get(self, request, *args, **kwargs):
        try:
            asyncio.run(self.run_bot())
            return HttpResponse("Bot is running")
        except Exception as e:
            return HttpResponse(f"Error starting bot: {str(e)}", status=500)

    async def run_bot(self):
        """Run the bot."""
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex('^🛋 Buyurtma berish$'), self.order_start)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_name)],
                PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_phone)],
                FURNITURE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_furniture_id)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )

        application.add_handler(CommandHandler("start", handle_start))
        application.add_handler(conv_handler)

        await application.initialize()
        await application.start()
        await application.run_polling(allowed_updates=Update.ALL_TYPES)