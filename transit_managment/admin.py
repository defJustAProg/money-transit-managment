from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin

from .models import Category, Status, Transaction, TransactionType


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'transaction_type', 'parent', 'description']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    mptt_level_indent = 20


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'status',
        'transaction_type',
        'category',
        'amount_display',
        'comment_short',
        'created_at',
    ]
    list_filter = ['status', 'transaction_type', 'category', 'date', 'created_at']
    search_fields = ['comment', 'category__name', 'status__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']

    fieldsets = (
        (
            'Основная информация',
            {'fields': ('date', 'status', 'transaction_type', 'category')},
        ),
        ('Финансовая информация', {'fields': ('amount', 'comment')}),
        (
            'Системная информация',
            {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)},
        ),
    )

    def amount_display(self, obj):
        """Отображение суммы с цветом"""
        if obj.transaction_type.name == 'Пополнение':
            return format_html(
                '<span style="color: green; font-weight: bold;">+{} ₽</span>',
                obj.amount,
            )
        else:
            return format_html('<span style="color: red; font-weight: bold;">-{} ₽</span>', obj.amount)

    amount_display.short_description = 'Сумма'

    def comment_short(self, obj):
        """Краткое отображение комментария"""
        if obj.comment:
            return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
        return '—'

    comment_short.short_description = 'Комментарий'

    def get_queryset(self, request):
        """Оптимизация запросов"""
        return super().get_queryset(request).select_related('status', 'transaction_type', 'category')
