from django.contrib import admin
from .models import Language, Material, Userdetail, Payment, Interest, Favouritetopic, Contact


class MaterialForm(admin.ModelAdmin):
    list_display = ('your_language', 'foreign_language', 'file', 'name', 'type')
    search_fields = ('language__name', 'name')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')

admin.site.register(Material, MaterialForm)
admin.site.register(Language)
admin.site.register(Userdetail)
admin.site.register(Payment)
admin.site.register(Interest)
admin.site.register(Favouritetopic)
admin.site.register(Contact, ContactAdmin)
