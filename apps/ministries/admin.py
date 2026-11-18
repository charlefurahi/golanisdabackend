from django.contrib import admin
from .models import Ministry

class SubMinistryInline(admin.TabularInline):
    model = Ministry
    fk_name = 'parent'
    extra = 0
    fields = ('name', 'leader', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True
    verbose_name = 'Sub-ministry'
    verbose_name_plural = 'Sub-ministries'


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'leader', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('leader', 'parent')
    autocomplete_fields = ()
    inlines = [SubMinistryInline]

    def get_inline_instances(self, request, obj=None):
        # Only show the "Sub-ministries" inline on major ministries (no parent
        # of their own) — a sub-ministry can't have children (one level deep).
        if obj and obj.parent_id is None:
            return super().get_inline_instances(request, obj)
        return []