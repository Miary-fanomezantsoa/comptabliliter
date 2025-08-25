from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from .models import (
    Currency, Tax, AccountTag, Account,
    Journal, JournalEntry, JournalItem,
    Company, UserProfile, HistoriqueModification, User, Partner, Product, OrderItem, Order, Payment,
    Invoice
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','role']

class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        # exclure explicitement tout ce qui peut poser problème
        # (relations ManyToMany implicites)
        extra_kwargs = {
            'groups': {'read_only': True},
            'user_permissions': {'read_only': True}
        }

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'

class CompteComptableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class HistoriqueModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueModification
        fields = '__all__'


class AccountTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTag
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False)  # <-- ici c'est facultatif
    class Meta:
        model = Account
        fields = ['id', 'code', 'name', 'account_type', 'currency',
                  'reconcile', 'note', 'taxes', 'tags', 'partner']

    def validate(self, data):
        # Crée une instance temporaire pour appeler clean()
        account = Account(**data)
        try:
            account.clean()  # Appelle la validation du modèle
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else str(e))
        return data

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'

class JournalItemSerializer(serializers.ModelSerializer):
    # Lecture complète
    account = AccountSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    entry = serializers.PrimaryKeyRelatedField(read_only=True)

    # Écriture : on fournit juste les IDs
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source='account',
        write_only=True
    )
    entry_id = serializers.PrimaryKeyRelatedField(
        queryset=JournalEntry.objects.all(),
        source='entry',
        write_only=True
    )
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        source='currency',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = JournalItem
        fields = [
            'id',
            'entry', 'entry_id',
            'account', 'account_id',
            'label', 'debit', 'credit',
            'currency', 'currency_id'
        ]


class JournalEntrySerializer(serializers.ModelSerializer):
    # Lecture
    journal = JournalSerializer(read_only=True)
    items = JournalItemSerializer(source='lines', many=True, read_only=True)

    # Écriture : fournir juste les IDs
    journal_id = serializers.PrimaryKeyRelatedField(
        queryset=Journal.objects.all(),
        source='journal',
        write_only=True
    )

    class Meta:
        model = JournalEntry
        fields = [
            'id',
            'date',
            'reference',
            'posted',
            'journal', 'journal_id',
            'items'
        ]

    def create(self, validated_data):
        # Création d'une entrée de journal
        journal_entry = JournalEntry.objects.create(
            journal=validated_data['journal'],
            date=validated_data.get('date'),
            reference=validated_data.get('reference', ''),
            posted=validated_data.get('posted', False)
        )
        return journal_entry

    def update(self, instance, validated_data):
        # Mise à jour simple des champs principaux
        instance.journal = validated_data.get('journal', instance.journal)
        instance.date = validated_data.get('date', instance.date)
        instance.reference = validated_data.get('reference', instance.reference)
        instance.posted = validated_data.get('posted', instance.posted)
        instance.save()
        return instance


class CompanySerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'
        extra_kwargs = {
            'company': {'required': False}
        }
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# ==== Invoice ====
class InvoiceSerializer(serializers.ModelSerializer):
    partner = serializers.StringRelatedField(read_only=True)
    partner_id = serializers.PrimaryKeyRelatedField(
        queryset=Partner.objects.all(),
        source='partner',
        write_only=True
    )
    tax = serializers.StringRelatedField(read_only=True)
    tax_id = serializers.PrimaryKeyRelatedField(
        queryset=Tax.objects.all(),
        source='tax',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'date', 'amount', 'status', 'tax', 'tax_id', 'partner', 'partner_id']


# ==== Order ====
class OrderSerializer(serializers.ModelSerializer):
    partner = serializers.StringRelatedField(read_only=True)
    partner_id = serializers.PrimaryKeyRelatedField(
        queryset=Partner.objects.all(),
        source='partner',
        write_only=True
    )
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Order
        fields = ['id', 'date', 'status', 'due_date', 'partner', 'partner_id', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        print("Données items reçues:", items_data)  # debug

        # Ajouter date par défaut si nécessaire
        if 'date' not in validated_data:
            validated_data['date'] = timezone.now().date()

        order = Order.objects.create(**validated_data)

        for item in items_data:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.get('quantity', 1)
            )
        return order



# ==== OrderItem ====
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_id', 'quantity']


# ==== Payment ====
class PaymentSerializer(serializers.ModelSerializer):
    partner = serializers.StringRelatedField(read_only=True)
    pattern_id = serializers.PrimaryKeyRelatedField(
        queryset=Partner.objects.all(),
        source='pattern',
        write_only=True
    )

    class Meta:
        model = Payment
        fields = ['id', 'payment_number', 'type', 'mode', 'description', 'date', 'amount', 'partner', 'pattern_id']

