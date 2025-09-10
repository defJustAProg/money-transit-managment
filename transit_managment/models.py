from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Status(models.Model):
    """Статус операции (Бизнес, Личное, Налог)"""

    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['name']

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    """Тип операции (Пополнение, Списание)"""

    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(MPTTModel):
    """Категория с древовидной структурой"""

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип операции',
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ['name', 'transaction_type', 'parent']

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Запись о движении денежных средств"""

    date = models.DateTimeField(default=timezone.now, verbose_name='Дата операции')
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Статус',
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Тип операции',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Категория',
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Сумма (руб.)',
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y")} - {self.amount} руб. ({self.status.name})'

    def clean(self):
        """Валидация логических зависимостей"""
        from django.core.exceptions import ValidationError

        # Проверяем, что категория относится к выбранному типу операции
        if self.category and self.transaction_type:
            if self.category.transaction_type != self.transaction_type:
                raise ValidationError(
                    f"Категория '{self.category.name}' не относится к типу операции '{self.transaction_type.name}'"
                )

        # Проверяем, что категория не является родительской (только листья дерева)
        if self.category and self.category.get_children().exists():
            raise ValidationError(
                f"Нельзя выбрать родительскую категорию '{self.category.name}'. Выберите подкатегорию."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
