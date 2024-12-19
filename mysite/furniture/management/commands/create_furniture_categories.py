from django.core.management.base import BaseCommand
from furniture.models import FurnitureCategory

class Command(BaseCommand):
    help = 'Creates initial furniture categories'

    def handle(self, *args, **kwargs):
        categories = [
            "Спальный гарнитур",
            "Шкаф",
            "Кровати",
            "Трюмо и камоды",
            "Прихожая",
            "Писменные столы",
            "Журнальный столик",
            "Столы стулья",
            "Диваны местного производства",
            "Диваны импортные премиум класса"
        ]

        for category_name in categories:
            FurnitureCategory.objects.get_or_create(name=category_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully created category "{category_name}"'))

