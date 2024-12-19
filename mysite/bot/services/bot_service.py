from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)
from django.conf import settings
from .constants import NAME, PHONE, FURNITURE_ID
from .handlers import (
    start_command,
    order_start,
    get_name,
    get_phone,
    get_furniture_id,
    cancel
)
import logging
import asyncio

logger = logging.getLogger(__name__)

class TelegramBotService:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        if not self.token:
            raise ValueError("Telegram bot token not found in settings")
        self.application = None

    def create_application(self) -> Application:
        if not self.application:
            self.application = Application.builder().token(self.token).build()

            conv_handler = ConversationHandler(
                entry_points=[
                    MessageHandler(
                        filters.Regex('^🛋 Buyurtma berish$'),
                        order_start
                    )
                ],
                states={
                    NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
                    PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
                    FURNITURE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_furniture_id)],
                },
                fallbacks=[CommandHandler('cancel', cancel)],
            )

            self.application.add_handler(CommandHandler("start", start_command))
            self.application.add_handler(conv_handler)

        return self.application

    async def start(self):
        try:
            application = self.create_application()
            await application.initialize()
            await application.start()
            logger.info("Bot started successfully")
            return application
        except Exception as e:
            logger.error(f"Failed to start bot: {str(e)}", exc_info=True)
            raise

    async def stop(self):
        if self.application:
            try:
                await self.application.stop()
                await self.application.shutdown()
                logger.info("Bot stopped successfully")
            except Exception as e:
                logger.error(f"Failed to stop bot: {str(e)}", exc_info=True)
                raise

    async def run(self):
        try:
            application = await self.start()
            await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error running bot: {str(e)}", exc_info=True)
            raise
        finally:
            await self.stop()

