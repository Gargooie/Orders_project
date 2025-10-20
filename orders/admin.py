from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'status', 'created_date', 'ready_date']
    list_filter = ['status', 'volume_type', 'created_date']
    search_fields = ['title', 'user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_date']
    list_editable = ['status']  # Позволяет редактировать статус прямо в списке
    list_per_page = 25  # Показывать по 25 заказов на странице
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'title', 'status')
        }),
        ('Детали заказа', {
            'fields': ('volume_type', 'description', 'document', 'quantity')
        }),
        ('Даты', {
            'fields': ('created_date', 'ready_date')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['user', 'volume_type']
        return self.readonly_fields
