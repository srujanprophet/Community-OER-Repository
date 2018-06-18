from django.db import models
#from django.contrib.auth.models import User


class Articles(models.Model):
    article_id = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.CharField(max_length=50, default='000000')
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    community = models.CharField(max_length=50, default='0000')



    def __str__(self):
        return self.title

    class Meta:
        db_table = "test_articles"
        verbose_name = "Article"
        verbose_name_plural = "Articles"


"""class Sales(models.Model):
    product = models.ForeignKey(Products, on_delete=None)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=18, decimal_places=2)
    #customer = models.ForeignKey(User, on_delete=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super(Sales, self).save(*args, **kwargs)

    class Meta:
        db_table = "tutorial_product_sales"
        verbose_name = "Sale"
        verbose_name_plural = "Sales"
"""