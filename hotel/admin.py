from django.contrib import admin

from hotel.models import Hotel, BookingModels, Comment, HotelImage


class HotelImageInLine(admin.TabularInline):
    model = HotelImage
    fields = ['image']


class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInLine]


admin.site.register(Hotel, HotelAdmin)
admin.site.register(BookingModels)
admin.site.register(Comment)
