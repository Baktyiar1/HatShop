from django.contrib import admin

from .models import Cap, Category, Image, Brand, Cart, Banner, Size
class BasketAdmin(admin.ModelAdmin):
    readonly_fields = ('unique_code',)

admin.site.register(Cap)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Brand)
admin.site.register(Cart, BasketAdmin)
admin.site.register(Banner)
admin.site.register(Size)
