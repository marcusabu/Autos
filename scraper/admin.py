from django.contrib import admin
from scraper.models import Auto
from django.utils.html import format_html


class AutoAdmin(admin.ModelAdmin):
    list_display = [field.name if field.name is not 'url' else 'visit' for field in Auto._meta.get_fields() ]
    list_filter = ('bouwjaar', 'is_handgeschakeld', 'is_benzine', 'bron')
    list_display_links = ('titel',)

    def visit(self, obj):
        return format_html("<a href='{}' target='_blank'>Open</a>".format(obj.url))

    def has_add_permission(self, request):
        return False


admin.site.register(Auto, AutoAdmin)
