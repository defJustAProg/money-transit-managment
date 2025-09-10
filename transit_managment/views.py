import logging

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from transit_managment.filters import TransactionFilter

from .models import Category, Status, Transaction, TransactionType
from .serializers import (
    CategorySerializer,
    CategoryTreeSerializer,
    StatusSerializer,
    TransactionCreateUpdateSerializer,
    TransactionSerializer,
    TransactionTypeSerializer,
)

logger = logging.getLogger('default')


class StatusViewSet(viewsets.ModelViewSet):
    """ViewSet для управления статусами"""

    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [AllowAny]


class TransactionTypeViewSet(viewsets.ModelViewSet):
    """ViewSet для управления типами операций"""

    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для управления категориями"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Получение дерева категорий"""
        root_categories = Category.objects.filter(parent=None)
        serializer = CategoryTreeSerializer(root_categories, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Получение категорий по типу операции"""
        transaction_type_id = request.query_params.get('transaction_type')
        if transaction_type_id:
            categories = Category.objects.filter(transaction_type_id=transaction_type_id)
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            return Response(serializer.data)
        return Response([])


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet для управления транзакциями"""

    queryset = Transaction.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TransactionCreateUpdateSerializer
        return TransactionSerializer

    def get_queryset(self):
        """Фильтрация транзакций"""
        queryset = Transaction.objects.all()
        transaction_filter = TransactionFilter(self.request.query_params, queryset=queryset)
        queryset = transaction_filter.qs

        return queryset.order_by('-date', '-created_at')

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Получение статистики по транзакциям"""
        queryset = self.get_queryset()

        total_income = queryset.filter(transaction_type__name='Пополнение').aggregate(total=Sum('amount'))['total'] or 0

        total_expense = queryset.filter(transaction_type__name='Списание').aggregate(total=Sum('amount'))['total'] or 0

        balance = total_income - total_expense

        return Response(
            {
                'total_income': total_income,
                'total_expense': total_expense,
                'balance': balance,
                'transaction_count': queryset.count(),
            }
        )


# Django Views для фронтенда
def home(request):
    """Главная страница с таблицей транзакций"""
    transactions = Transaction.objects.all().order_by('-date', '-created_at')
    transaction_filter = TransactionFilter(request.GET, queryset=transactions)
    transactions = transaction_filter.qs

    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.all(),
        'filters': {
            'date_from': request.GET.get('date_from'),
            'date_to': request.GET.get('date_to'),
            'status_id': request.GET.get('status'),
            'transaction_type_id': request.GET.get('transaction_type'),
            'category_id': request.GET.get('category'),
        },
    }

    return render(request, 'transit_managment/home.html', context)


def transaction_create(request):
    """Создание новой транзакции"""
    if request.method == 'POST':
        form_data = request.POST
        try:
            transaction = Transaction.objects.create(
                date=form_data.get('date'),
                status_id=form_data.get('status'),
                transaction_type_id=form_data.get('transaction_type'),
                category_id=form_data.get('category'),
                amount=form_data.get('amount'),
                comment=form_data.get('comment', ''),
            )
            messages.success(request, 'Транзакция успешно создана!')
            return redirect('transit_managment:home')
        except Exception as e:
            messages.error(request, f'Ошибка при создании транзакции: {str(e)}')
            logger.exception(e)

    context = {
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'transit_managment/transaction_form.html', context)


def transaction_edit(request, pk):
    """Редактирование транзакции"""
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form_data = request.POST
        try:
            transaction.date = form_data.get('date')
            transaction.status_id = form_data.get('status')
            transaction.transaction_type_id = form_data.get('transaction_type')
            transaction.category_id = form_data.get('category')
            transaction.amount = form_data.get('amount')
            transaction.comment = form_data.get('comment', '')
            transaction.save()
            messages.success(request, 'Транзакция успешно обновлена!')
            return redirect('transit_managment:home')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении транзакции: {str(e)}')
            logger.exception(e)

    context = {
        'transaction': transaction,
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'transit_managment/transaction_form.html', context)


def transaction_delete(request, pk):
    """Удаление транзакции"""
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Транзакция успешно удалена!')
        return redirect('transit_managment:home')

    context = {'transaction': transaction}
    return render(request, 'transit_managment/transaction_confirm_delete.html', context)


def reference_management(request):
    """Управление справочниками"""
    context = {
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'transit_managment/reference_management.html', context)


# API endpoints для AJAX запросов
def get_categories_by_type(request):
    """Получение категорий по типу операции для AJAX"""
    transaction_type_id = request.GET.get('transaction_type')
    if transaction_type_id:
        categories = Category.objects.filter(transaction_type_id=transaction_type_id)
        data = [{'id': cat.id, 'name': cat.name} for cat in categories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)
