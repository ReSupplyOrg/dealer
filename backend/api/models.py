from django.db import models
import uuid

# Create your models here.
class Clients(models.Model):
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)
    deletion = models.DateTimeField(auto_now=True)
    phone = models.TextField()
    confirmed = models.BooleanField(default=False)
    image_bytes = models.ImageField(null=True, max_length=10000)
    names = models.TextField()
    username = models.TextField()
    password_salt =  models.BinaryField()
    password_hash = models.BinaryField()
    
    def __str__(self):
        return '{} {} {} {} {}'.format(self.uuid, self.phone, self.username, self.names, self.password_hash)
    
    class Meta:
        ordering = ['-creation']

class Stores(models.Model):
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)
    deletion = models.DateTimeField(auto_now=True)
    phone = models.TextField()
    confirmed = models.BooleanField(default=False)
    image_bytes = models.ImageField(null=True)
    name = models.TextField()
    rating = models.FloatField(default=0)
    address = models.TextField()
    username = models.TextField()
    password_salt =  models.BinaryField()
    password_hash = models.BinaryField()
    latitude = models.FloatField(null = True)
    longitude = models.FloatField(null = True)

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.uuid, self.phone, self.username, self.name, self.address, self.password_hash)

    class Meta:
        ordering = ['-creation']

class Ratings(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)
    deletion = models.DateTimeField(auto_now=True)
    client_uuid = models.ForeignKey(Clients, on_delete=models.CASCADE)
    store_uuid = models.ForeignKey(Stores, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return '{} {} {}'.format(self.client_uuid, self.store_uuid, self.rating)

    class Meta:
        ordering = ['-creation']

class Packs(models.Model):
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)
    deletion = models.DateTimeField(auto_now=True)
    image_bytes = models.ImageField(null=True)
    owner = models.ForeignKey(Stores, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    name = models.TextField()

    STATUS_CHOICES = [
        ('fast_food', 'Fast food'),
        ('dessert', 'Dessert'),
        ('random', 'Random'),
    ]
    pack_type = models.CharField(max_length=20, choices=STATUS_CHOICES, default="random")

    description = models.TextField()

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.uuid, self.owner, self.stock, self.price, self.name, self.description)

    class Meta:
        ordering = ['-creation']

class Orders(models.Model):
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)
    deletion = models.DateTimeField(auto_now=True)
    client_uuid = models.ForeignKey(Clients, on_delete=models.CASCADE)
    store_uuid = models.ForeignKey(Stores, on_delete=models.CASCADE)
    pack_uuid = models.ForeignKey(Packs, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payed_price = models.IntegerField()

    def __str__(self):
        return '{} {} {} {} {}'.format(self.uuid, self.client_uuid, self.store_uuid, self.pack_uuid, self.payed_price)
    
    class Meta:
        ordering = ['-creation']

