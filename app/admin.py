from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced
# Register your models here.


@admin.register(Customer)
class customerModelAdmin (admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class productModelAdmin (admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','decription','brand','category','product_image']

@admin.register(Cart)
class cartModelAdmin (admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class orderModelAdmin (admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status']