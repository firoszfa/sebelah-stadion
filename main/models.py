from django.db import models

# Create your models here.
class Products(models.Model):
    CATEGORY_PRODUCT = [
        ('jersey', 'Jersey'),
        ('sepatu', 'Sepatu'),
        ('tiket', 'Tiket'),
        ('aksesoris', 'Aksesoris'),
        ('makanan', 'Makanan'),
        ('minuman', 'Minuman'),
        ('dll', 'DLL'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    stock = models.PositiveIntegerField(default=1)
    thumbnail = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_PRODUCT, default='dll')
    is_featured = models.BooleanField(default=False)
