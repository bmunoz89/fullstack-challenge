from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('name', )


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    thumbnail_url = models.URLField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.BooleanField()
    product_description = models.TextField()
    upc = models.CharField(max_length=16)
    last_modified = models.DateTimeField(default=None, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE)

    class Meta:
        ordering = ('title', )
