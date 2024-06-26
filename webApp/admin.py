from django.contrib import admin
from .models import Category,Product,Cart,Orders,Slider
from django.utils import timezone
from django import forms


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'  

class SliderAdmin(admin.ModelAdmin):
    form = SliderForm  # Use the custom form for Slider model
    list_display = ('title', 'image', 'status', 'duration')
    def save_model(self, request, obj, form, change):
        if not obj.duration:  # If duration field is empty
            obj.duration = timezone.now()  # Set duration to current time
        obj.save()


class CartAdmin(admin.ModelAdmin):
    list_display=('user','product','product_quantity')


class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','description','image','status')

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','original_price','selling_price','quantity')

class ProductOrdered(admin.ModelAdmin):
    list_display=('id','name','user_id','number','alt_number','address','product_id','selling_price','product_quantity','total_amount','payment_type','date')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Orders,ProductOrdered)
admin.site.register(Slider,SliderAdmin)
