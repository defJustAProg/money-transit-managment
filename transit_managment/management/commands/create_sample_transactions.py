from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from transit_managment.models import Category, Status, Transaction, TransactionType


class Command(BaseCommand):
    help = 'Создает примеры транзакций для демонстрации'

    def handle(self, *args, **options):
        # Получение объектов
        business_status = Status.objects.get(name='Бизнес')
        personal_status = Status.objects.get(name='Личное')

        income_type = TransactionType.objects.get(name='Пополнение')
        expense_type = TransactionType.objects.get(name='Списание')

        # Категории доходов
        salary = Category.objects.get(name='Зарплата', transaction_type=income_type)
        freelance = Category.objects.get(name='Фриланс', transaction_type=income_type)

        # Категории расходов
        vps = Category.objects.get(name='VPS', transaction_type=expense_type)
        proxy = Category.objects.get(name='Proxy', transaction_type=expense_type)
        farpost = Category.objects.get(name='Farpost', transaction_type=expense_type)
        avito = Category.objects.get(name='Avito', transaction_type=expense_type)
        food = Category.objects.get(name='Продукты питания', transaction_type=expense_type)
        transport = Category.objects.get(name='Транспорт', transaction_type=expense_type)

        # Создание примеров транзакций
        sample_transactions = [
            # Доходы
            {
                'date': timezone.now() - timedelta(days=1),
                'status': business_status,
                'transaction_type': income_type,
                'category': salary,
                'amount': 50000.00,
                'comment': 'Зарплата за январь',
            },
            {
                'date': timezone.now() - timedelta(days=3),
                'status': business_status,
                'transaction_type': income_type,
                'category': freelance,
                'amount': 15000.00,
                'comment': 'Проект по разработке сайта',
            },
            {
                'date': timezone.now() - timedelta(days=5),
                'status': personal_status,
                'transaction_type': income_type,
                'category': freelance,
                'amount': 8000.00,
                'comment': 'Консультация по SEO',
            },
            # Расходы
            {
                'date': timezone.now() - timedelta(days=2),
                'status': business_status,
                'transaction_type': expense_type,
                'category': vps,
                'amount': 2500.00,
                'comment': 'VPS сервер на месяц',
            },
            {
                'date': timezone.now() - timedelta(days=4),
                'status': business_status,
                'transaction_type': expense_type,
                'category': proxy,
                'amount': 1200.00,
                'comment': 'Прокси для парсинга',
            },
            {
                'date': timezone.now() - timedelta(days=6),
                'status': business_status,
                'transaction_type': expense_type,
                'category': farpost,
                'amount': 5000.00,
                'comment': 'Реклама на Farpost',
            },
            {
                'date': timezone.now() - timedelta(days=7),
                'status': business_status,
                'transaction_type': expense_type,
                'category': avito,
                'amount': 3000.00,
                'comment': 'Реклама на Avito',
            },
            {
                'date': timezone.now() - timedelta(days=1),
                'status': personal_status,
                'transaction_type': expense_type,
                'category': food,
                'amount': 2500.00,
                'comment': 'Продукты на неделю',
            },
            {
                'date': timezone.now() - timedelta(days=2),
                'status': personal_status,
                'transaction_type': expense_type,
                'category': transport,
                'amount': 800.00,
                'comment': 'Проезд на работу',
            },
            {
                'date': timezone.now() - timedelta(days=8),
                'status': personal_status,
                'transaction_type': expense_type,
                'category': food,
                'amount': 1800.00,
                'comment': 'Обед в ресторане',
            },
        ]

        for transaction_data in sample_transactions:
            transaction, created = Transaction.objects.get_or_create(
                date=transaction_data['date'],
                status=transaction_data['status'],
                transaction_type=transaction_data['transaction_type'],
                category=transaction_data['category'],
                amount=transaction_data['amount'],
                defaults={'comment': transaction_data['comment']},
            )
