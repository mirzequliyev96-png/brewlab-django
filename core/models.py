from django.db import models
from django.core.validators import RegexValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('preparing', 'Hazırlanır'),
        ('delivered', 'Çatdırıldı'),
        ('cancelled', 'Ləğv edildi'),
    ]
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField( max_length=20,
                                      validators=[RegexValidator(
                                          regex=r'^\d{9,15}$',
                                          message="Nömrə ən azı 9 rəqəmdən ibarət olmalıdır, yalnız rəqəm yazın"
                                      )])
    customer_address = models.CharField(max_length=255) #, blank=True) - eyer istesen ki unvan yazmaq mecburi olsun #-i gotur bunu koda birleshdir.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_amount(self):
        return sum(item.price * item.quantity for item in self.items.all())
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # sifariş anındakı qiymət
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"