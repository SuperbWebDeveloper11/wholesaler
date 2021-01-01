from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django_resized import ResizedImageField

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    owner = models.ForeignKey('auth.User', related_name='categories', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('announce:category_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Announce(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='announce_images', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    tags = TaggableManager()

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='announces', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='announces', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('announce:announce_detail', kwargs={'pk': self.pk})
                     
    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    body = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)

    announce = models.ForeignKey(Announce, related_name='comments', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']


