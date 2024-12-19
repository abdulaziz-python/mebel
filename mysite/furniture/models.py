import random
from django.db import models
from .constants import ORDER_STATUS_CHOICES, PRICE_MAX_DIGITS, PRICE_DECIMAL_PLACES, FURNITURE_CATEGORIES

class FurnitureImage(models.Model):
    furniture = models.ForeignKey('Furniture', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='furniture_images/')
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Картина {self.id} - {self.furniture.name}"
    
    class Meta:
        ordering = ['order']

class Furniture(models.Model):
    furniture_id = models.CharField(max_length=4, unique=True, editable=False)
    name = models.CharField(max_length=200, verbose_name="Название мебели")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        verbose_name="Цена (сум)"
    )
    video_link = models.URLField(verbose_name="Ссылка на видео")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=20,
        choices=FURNITURE_CATEGORIES,
        verbose_name="Категория",
        default='bedroom'  # Add this line
    )

    def save(self, *args, **kwargs):
        if not self.furniture_id:
            while True:
                new_id = str(random.randint(1000, 9999))
                if not Furniture.objects.filter(furniture_id=new_id).exists():
                    self.furniture_id = new_id
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.furniture_id}"
    
    class Meta:
        verbose_name = "Мебель"
        verbose_name_plural = "Мебель"

class Order(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200, verbose_name="Имя клиента")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer_name} - {self.furniture.name}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

