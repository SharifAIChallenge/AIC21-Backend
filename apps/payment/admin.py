from django.contrib import admin

from .models import PaymentRequest, PaymentConfig


# Register your models here.

@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'description', 'user', 'callback_url',
                    'authority', 'ref_id')
    list_display_links = ('id',)

    sortable_by = ('id', 'ref_id')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(PaymentConfig)
class PaymentConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'description')
    list_display_links = ('id',)
    list_editable = ('amount', 'description')
