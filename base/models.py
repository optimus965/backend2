from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)#Set the foreign key to NULL when the referenced object i.e parent table user is deleted. 
    name=models.CharField(max_length=200,null=True,blank=True)
    image=models.ImageField(null=True, blank=True,default='/placeholder.png') #to work this install pillow i.e python -m pip install Pillow
    brand=models.CharField(max_length=200,null=True,blank=True)
    category=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    rating=models.DecimalField(max_digits=7,decimal_places=2,default=0,null=True,blank=True)
    numReviews=models.IntegerField(null=True, blank=True)
    price=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    countInStock=models.IntegerField(null=True, blank=True, default=0)
    createdAt=models.DateTimeField(auto_now_add=True)
    _id=models.AutoField(primary_key=True,editable=False) #user will acts as id but i need to over ride so telling take this as primary key and AutoField: An integer field that automatically increments, typically used as a primary key.
    def __str__(self):
        return self.name

class Review(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True) #foreign key is many to one replationship i.e one product can have many reviews
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    rating=models.IntegerField(null=True, blank=True,default=0)
    comment=models.TextField(null=True, blank=True)
    createdAt=models.DateTimeField(auto_now_add=True)
    _id=models.AutoField(primary_key=True,editable=False) #user will acts as id but i need to over ride so telling take this as primary key and AutoField: An integer field that automatically increments, typically used as a primary key.
    
    def __str__(self):
        return str(self.rating)


class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    paymentMethod=models.CharField(max_length=200,null=True,blank=True)
    taxPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    shippingPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    totalPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    isPaid=models.BooleanField(default=False)
    paidAt=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    isDelivered=models.BooleanField(default=False)
    deliveredAt=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    createdAt=models.DateTimeField(auto_now_add=True)
    _id=models.AutoField(primary_key=True,editable=False) #user will acts as id but i need to over ride so telling take this as primary key and AutoField: An integer field that automatically increments, typically used as a primary key.

    def __str__(self):
        return str(self.createdAt)
    
#each order has multiple items
class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True) #to know item product
    order=models.ForeignKey(Order, on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    qty=models.IntegerField(null=True, blank=True)
    price=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    image=models.CharField(max_length=200,null=True,blank=True)
    _id=models.AutoField(primary_key=True,editable=False) #user will acts as id but i need to over ride so telling take this as primary key and AutoField: An integer field that automatically increments, typically used as a primary key.
    
    def __str__(self):
         return str(self.name)


class ShippingAddress(models.Model):
    order=models.OneToOneField(Order,on_delete=models.CASCADE,null=True,blank=True)#one order can have only one shipping address
    address=models.CharField(max_length=200,null=True,blank=True)
    city=models.CharField(max_length=200,null=True,blank=True)
    postalCode=models.CharField(max_length=200,null=True,blank=True)
    country=models.CharField(max_length=200,null=True,blank=True)
    shippingPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    _id=models.AutoField(primary_key=True,editable=False) #user will acts as id but i need to over ride so telling take this as primary key and AutoField: An integer field that automatically increments, typically used as a primary key.
    
    def __str__(self):
         return str(self.address)
    