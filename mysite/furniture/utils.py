
import random
from .models import Furniture

def generate_furniture_id():
    while True:
        new_id = str(random.randint(1000, 9999))
        if not Furniture.objects.filter(furniture_id=new_id).exists():
            return new_id