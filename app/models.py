from django.db import models
from  django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.db.models.deletion import CASCADE
from phonenumber_field.modelfields import PhoneNumberField

STATE_CHOICE = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

class Customer(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICE,max_length=100)
    phone = PhoneNumberField()
    # otp=models.CharField(max_length=6,default=0)
    def __str__(self):
            return str(self.id)

CATEGORY_CHOICES=(('S','sofa'),('C','chair'),('T','table'))

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    
    description=models.TextField()
    
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    product=models.ForeignKey(Product,on_delete=CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

STATUS_CHOICE=(('Accepted','Accepted'),('Packed','Packed'),('On the way','On the way'),('Delivered','Delivered'),('Cancel','Cancel'))

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    Customer=models.ForeignKey(Customer,on_delete=CASCADE)
    product=models.ForeignKey(Product,on_delete=CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICE,default='Pending')

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

    
