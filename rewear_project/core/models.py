from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    # Django's built-in User model already has username, email, password, etc.
    # We add the 'points' field here.
    points = models.IntegerField(default=50)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.name

class Item(models.Model):
    # Choices for fields, making data consistent
    CATEGORY_CHOICES = [
        ('tops', 'Tops'), ('bottoms', 'Bottoms'), ('dresses', 'Dresses'),
        ('outerwear', 'Outerwear'), ('shoes', 'Shoes'), ('accessories', 'Accessories')
    ]
    SIZE_CHOICES = [
        ('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL')
    ]
    CONDITION_CHOICES = [
        ('new', 'New with tags'), ('excellent', 'Excellent'),
        ('good', 'Good'), ('fair', 'Fair')
    ]
    STATUS_CHOICES = [
        ('available', 'Available'), ('swapped', 'Swapped')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    
    
    # Relationships
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    tags = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='item_images/', default='item_images/default.png')

    # Admin and creation fields
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.uploader.username}'
    