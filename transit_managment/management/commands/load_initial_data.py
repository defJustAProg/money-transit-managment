from django.core.management.base import BaseCommand

from transit_managment.models import Category, Status, TransactionType


class Command(BaseCommand):
    help = 'Загружает начальные данные для системы ДДС'

    def handle(self, *args, **options):
        statuses_data = [
            {'name': 'Бизнес', 'description': 'Бизнес операции'},
            {'name': 'Личное', 'description': 'Личные операции'},
            {'name': 'Налог', 'description': 'Налоговые операции'},
        ]

        for status_data in statuses_data:
            status, created = Status.objects.get_or_create(
                name=status_data['name'],
                defaults={'description': status_data['description']},
            )

        # Создание типов операций
        types_data = [
            {'name': 'Пополнение', 'description': 'Поступление денежных средств'},
            {'name': 'Списание', 'description': 'Расход денежных средств'},
        ]

        for type_data in types_data:
            transaction_type, created = TransactionType.objects.get_or_create(
                name=type_data['name'],
                defaults={'description': type_data['description']},
            )

        # Получение объектов для создания категорий
        income_type = TransactionType.objects.get(name='Пополнение')
        expense_type = TransactionType.objects.get(name='Списание')

        # Создание категорий для пополнений
        income_categories = [
            {'name': 'Зарплата', 'description': 'Заработная плата'},
            {'name': 'Фриланс', 'description': 'Доходы от фриланса'},
            {'name': 'Инвестиции', 'description': 'Доходы от инвестиций'},
            {'name': 'Продажи', 'description': 'Доходы от продаж'},
        ]

        for cat_data in income_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                transaction_type=income_type,
                defaults={'description': cat_data['description']},
            )

        # Создание категорий для списаний
        expense_categories = [
            {'name': 'Инфраструктура', 'description': 'Расходы на инфраструктуру'},
            {'name': 'Маркетинг', 'description': 'Маркетинговые расходы'},
            {'name': 'Продукты питания', 'description': 'Расходы на еду'},
            {'name': 'Транспорт', 'description': 'Транспортные расходы'},
            {'name': 'Развлечения', 'description': 'Расходы на развлечения'},
        ]

        for cat_data in expense_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                transaction_type=expense_type,
                defaults={'description': cat_data['description']},
            )

        # Создание подкатегорий для инфраструктуры
        infrastructure = Category.objects.get(name='Инфраструктура', transaction_type=expense_type)
        infrastructure_subcategories = [
            {'name': 'VPS', 'description': 'Виртуальные серверы'},
            {'name': 'Proxy', 'description': 'Прокси серверы'},
            {'name': 'Домен', 'description': 'Регистрация и продление доменов'},
        ]

        for subcat_data in infrastructure_subcategories:
            subcategory, created = Category.objects.get_or_create(
                name=subcat_data['name'],
                transaction_type=expense_type,
                parent=infrastructure,
                defaults={'description': subcat_data['description']},
            )

        # Создание подкатегорий для маркетинга
        marketing = Category.objects.get(name='Маркетинг', transaction_type=expense_type)
        marketing_subcategories = [
            {'name': 'Farpost', 'description': 'Реклама на Farpost'},
            {'name': 'Avito', 'description': 'Реклама на Avito'},
            {'name': 'Google Ads', 'description': 'Реклама в Google'},
            {'name': 'Яндекс.Директ', 'description': 'Реклама в Яндекс.Директ'},
        ]

        for subcat_data in marketing_subcategories:
            subcategory, created = Category.objects.get_or_create(
                name=subcat_data['name'],
                transaction_type=expense_type,
                parent=marketing,
                defaults={'description': subcat_data['description']},
            )
