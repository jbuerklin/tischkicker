from django.contrib import admin
from braschuene.models import Debt


# Register your models here.
@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ("amount", "date", "get_senders", "get_receivers", "note", "done")
    list_filter = ("date", "done")
    search_fields = ("note",)
    actions = ["mark_as_done", "mark_as_not_done"]

    def mark_as_done(self, request, queryset):
        queryset.update(done=True)

    def mark_as_not_done(self, request, queryset):
        queryset.update(done=False)
