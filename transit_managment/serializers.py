from rest_framework import serializers

from .models import Category, Status, Transaction, TransactionType


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий с древовидной структурой"""

    children = serializers.SerializerMethodField()
    transaction_type_name = serializers.CharField(source='transaction_type.name', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'transaction_type',
            'transaction_type_name',
            'parent',
            'parent_name',
            'children',
            'created_at',
            'updated_at',
        ]

    def get_children(self, obj):
        """Получение дочерних категорий"""
        children = obj.get_children()
        if children.exists():
            return CategorySerializer(children, many=True, context=self.context).data
        return []


class CategoryTreeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения дерева категорий"""

    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'children']

    def get_children(self, obj):
        """Получение дочерних категорий"""
        children = obj.get_children()
        if children.exists():
            return CategoryTreeSerializer(children, many=True, context=self.context).data
        return []


class TransactionSerializer(serializers.ModelSerializer):
    """Сериализатор для транзакций"""

    status_name = serializers.CharField(source='status.name', read_only=True)
    transaction_type_name = serializers.CharField(source='transaction_type.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    date_display = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'date',
            'date_display',
            'status',
            'status_name',
            'transaction_type',
            'transaction_type_name',
            'category',
            'category_name',
            'amount',
            'comment',
            'created_at',
            'updated_at',
        ]

    def get_date_display(self, obj):
        return obj.date.strftime('%d.%m.%Y %H:%M')

    def validate(self, data):
        """Валидация логических зависимостей"""
        category = data.get('category')
        transaction_type = data.get('transaction_type')

        if category and transaction_type:
            if category.transaction_type != transaction_type:
                raise serializers.ValidationError(
                    f"Категория '{category.name}' не относится к типу операции '{transaction_type.name}'"
                )

            # Проверяем, что категория не является родительской
            if category.get_children().exists():
                raise serializers.ValidationError(
                    f"Нельзя выбрать родительскую категорию '{category.name}'. Выберите подкатегорию."
                )

        return data


class TransactionCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления транзакций"""

    class Meta:
        model = Transaction
        fields = ['date', 'status', 'transaction_type', 'category', 'amount', 'comment']

    def validate(self, data):
        """Валидация логических зависимостей"""
        category = data.get('category')
        transaction_type = data.get('transaction_type')

        if category and transaction_type:
            if category.transaction_type != transaction_type:
                raise serializers.ValidationError(
                    f"Категория '{category.name}' не относится к типу операции '{transaction_type.name}'"
                )

            # Проверяем, что категория не является родительской
            if category.get_children().exists():
                raise serializers.ValidationError(
                    f"Нельзя выбрать родительскую категорию '{category.name}'. Выберите подкатегорию."
                )

        return data


class TransactionFilterSerializer(serializers.Serializer):
    """Сериализатор для фильтрации транзакций"""

    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), required=False)
    transaction_type = serializers.PrimaryKeyRelatedField(queryset=TransactionType.objects.all(), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
