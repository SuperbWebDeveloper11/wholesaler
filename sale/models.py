import json
import os
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'algeria_cities.json')

wilayas = []

with open(file_path) as json_file:
    data = json.load(json_file)
    for p in data['wilayas']:
        tup = (p['name'], p['name'])
        wilayas.append(tup)



class Category(models.Model):
    name = models.CharField(max_length=250)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories_created')

    def get_absolute_url(self):
        return reverse('sale:category_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name




class Mark(models.Model):
    name = models.CharField(max_length=250)
    country = CountryField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marks_created')

    def get_absolute_url(self):
        return reverse('sale:mark_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=250)
    wilaya = models.CharField(max_length=250, choices=wilayas)
    address = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='store_images/%Y/%m/%d/', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores_created')

    def get_absolute_url(self):
        return reverse('sale:store_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    mark = models.ForeignKey(Mark, on_delete=models.SET_NULL, related_name='products', null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products_created')

    def get_absolute_url(self):
        return reverse('sale:product_detail', kwargs={'store_pk': self.store.pk, 'pk': self.pk})

    def __str__(self):
        return self.name

class Cart(models.Model):
    # code = models.CharField(max_length=250)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products_created')

    def get_absolute_url(self):
        return reverse('sale:cart_detail', kwargs={'store_pk': self.store.pk, 'pk': self.pk})

    def __str__(self):
        return self.name

