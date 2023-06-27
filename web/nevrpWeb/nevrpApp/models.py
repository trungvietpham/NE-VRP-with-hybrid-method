from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Node(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(max_length=40)
    longitude = models.FloatField(max_length=40)
    address = models.CharField(max_length=400, null=True, blank=True)
    code = models.CharField(max_length=400, unique=True, primary_key=True)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=86400)
    name = models.CharField(max_length=400, null=True, blank=True)
    type = models.CharField(max_length=10, choices=(('gd1', 'GD1'), ('gd2', 'GD2'), ('gd3', 'GD3')))
    capacity = models.FloatField(max_length=40, default=1000)
    province_code = models.CharField(max_length=400, null=True)
    district_code = models.CharField(max_length=400, null=True)
    
    # slug = models.SlugField(unique=True, null=True, max_length=400)
    
    def get_absolute_url(self):
        return reverse('node-detail', kwargs={'pk': self.pk})
    
    def get_url(self):
        return "https://www.google.com/maps/place/" + str(self.latitude) + ',' + str(self.longitude)
    
    def save(self, *args, **kwargs):
        value = self.code
        # self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return '%s' %(self.pk)
    
class Order(models.Model):
    code = models.CharField(primary_key=True, max_length=400, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    capacity = models.FloatField(max_length=10, default=1.0)
    delivery_after_time = models.IntegerField(default=0)
    delivery_before_time = models.IntegerField(default=86400)
    delivery_mode = models.CharField(max_length=100, choices=(('standard','STANDARD'), ('rapid', 'RAPID')), default='standard')
    order_value = models.FloatField(max_length=400, null=True, blank=True)
    time_service = models.IntegerField(default=1, null=True)
    time_loading = models.IntegerField(default=1, null=True)
    weight = models.FloatField(max_length=400, null=True, blank=True)
    sender_code = models.ForeignKey(Node, related_name='sender_code', on_delete=models.CASCADE)
    receiver_code = models.ForeignKey(Node, related_name='receiver_code', on_delete=models.CASCADE)
    # slug = models.SlugField(unique=True, null=True, max_length=400)
    
    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        value = self.code
        # self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return '%s' %(self.code)
    
class Vehicle(models.Model):
    code = models.CharField(primary_key=True, max_length=400, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.CharField(max_length=5, choices=(('1','Rảnh'), ('0', 'Bận')), default='1')
    average_fee_transport = models.FloatField(max_length=10, default=0.1)
    average_gas_consume = models.FloatField(max_length=10, default=0.02)
    average_velocity = models.FloatField(max_length=10, default=60)
    driver_name = models.CharField(max_length=100, null=True, blank=True)
    gas_price = models.FloatField(max_length=10, default=23000)
    height = models.FloatField(max_length=10, null=True, blank=True)
    length = models.FloatField(max_length=10, null=True, blank=True)
    max_capacity = models.FloatField(max_length=10, default=500)
    max_load_weight = models.FloatField(max_length=10, null=True, blank=True)
    max_velocity = models.FloatField(max_length=10, null=True, blank=True)
    min_velocity = models.FloatField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, choices=(('1', 'Xe vận tải'), ('2', 'Xe tải 3 chỗ'), ('3', 'Xe tải 4 chỗ'), ('4', 'Xe máy'),), default='4')
    width = models.FloatField(max_length=10, null=True, blank=True)
    vehicle_cost = models.FloatField(max_length=10, null=True, blank=True)
    manager_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='manager')
    current_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='current')
    # slug = models.SlugField(unique=True, null=True, max_length=400)
    
    def get_absolute_url(self):
        return reverse('vehicle-detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        value = self.code
        # self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return '%s' %(self.code)