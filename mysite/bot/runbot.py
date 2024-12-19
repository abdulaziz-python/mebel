import asyncio
import logging
from django.core.management.base import BaseCommand
from services.bot_service import TelegramBotService

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Start the Telegram bot'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))
            bot_service = TelegramBotService()
            asyncio.run(bot_service.run())
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('\nBot stopped by user'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error running bot: {str(e)}')
            )
            logger.error("Bot error", exc_info=True)
        finally:
            # Ensure proper cleanup
            self.stdout.write(self.style.SUCCESS('Bot shutdown complete'))