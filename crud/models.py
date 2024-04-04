from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=30, decimal_places=2)
    quantity = models.IntegerField()  # One-to-Many
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):  # Many-to-Many
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if self.pk:  # Если объект уже существует (обновление)
            old_instance = Purchase.objects.get(pk=self.pk)
            product = Product.objects.get(pk=self.product.pk)
            product.quantity += old_instance.quantity
            product.quantity -= self.quantity
            product.save()
            balance = Balance.objects.get(user=self.user)
            balance.balance += old_instance.quantity * old_instance.product.price
            balance.balance -= self.quantity * self.product.price
            balance.save()
        else:
            product = Product.objects.get(pk=self.product.pk)
            product.quantity -= self.quantity
            product.save()
            balance = Balance.objects.get(user=self.user)
            balance.balance -= self.quantity * self.product.price
            balance.save()

    def delete(self, *args, **kwargs):
        product = Product.objects.get(pk=self.product.pk)
        product.quantity += self.quantity
        product.save()
        balance = Balance.objects.get(user=self.user)
        balance.balance += self.quantity * self.product.price
        balance.save()
        super(Purchase, self).delete(*args, **kwargs)


class Balance(models.Model):  # One-to-One
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} balance: {self.balance}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
