from django.contrib import admin
from .models import Language,Material,Userdetail,Payment , Interest , Favouritetopic

class MaterialForm(admin.ModelAdmin):
    list_display = ('your_language','foreign_language', 'file', 'name','type')
    search_fields = ('language__name', 'name')

admin.site.register(Material,MaterialForm)
admin.site.register(Language)
admin.site.register(Userdetail)
admin.site.register(Payment)
admin.site.register(Interest)
admin.site.register(Favouritetopic)