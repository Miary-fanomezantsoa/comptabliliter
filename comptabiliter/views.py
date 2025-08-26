from dal import autocomplete
from django.db.models import Sum
from rest_framework import viewsets, filters, serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
import json
from .models import (
    Currency, Tax, AccountTag, Account,
    Journal, JournalEntry, JournalItem, Partner,
    Company, UserProfile, HistoriqueModification, Order, Invoice, Product, OrderItem, Payment
)
from .serializers import (
    CurrencySerializer, TaxSerializer, AccountTagSerializer, AccountSerializer,
    JournalSerializer, JournalEntrySerializer, JournalItemSerializer, PartnerSerializer,
    CompanySerializer, UserProfileSerializer, UserSerializer, CompteComptableSerializer,
    HistoriqueModificationSerializer, SafeUserSerializer, PaymentSerializer, OrderItemSerializer, OrderSerializer,
    InvoiceSerializer, ProductSerializer
)

#devise
class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


#tax
class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


#journal

class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer

class JournalItemViewSet(viewsets.ModelViewSet):
    queryset = JournalItem.objects.all()
    serializer_class = JournalItemSerializer



#entreprise
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


#utilisateur
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = SafeUserSerializer(request.user)
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

#compte contable
class AccountTagViewSet(viewsets.ModelViewSet):
    queryset = AccountTag.objects.all()
    serializer_class = AccountTagSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CompteComptableViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('code')
    serializer_class = CompteComptableSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name',]
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        compte = serializer.save()
        HistoriqueModification.objects.create(
            compte=compte,
            utilisateur=self.request.user if self.request.user.is_authenticated else None,
            action="création",
            nouvelle_valeur=json.dumps(serializer.data)
        )

    def perform_update(self, serializer):
        instance = self.get_object()
        ancienne = CompteComptableSerializer(instance).data
        compte = serializer.save()
        HistoriqueModification.objects.create(
            compte=compte,
            utilisateur=self.request.user if self.request.user.is_authenticated else None,
            action="modification",
            ancienne_valeur=json.dumps(ancienne),
            nouvelle_valeur=json.dumps(serializer.data)
        )

    def perform_destroy(self, instance):
        HistoriqueModification.objects.create(
            compte=instance,
            utilisateur=self.request.user if self.request.user.is_authenticated else None,
            action="suppression",
            ancienne_valeur=json.dumps(CompteComptableSerializer(instance).data)
        )
        instance.delete()

    @action(detail=True, methods=['get'])
    def historique(self, request, pk=None):
        compte = self.get_object()
        historique = HistoriqueModification.objects.filter(compte=compte)
        serializer = HistoriqueModificationSerializer(historique, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def ecritures(self, request, pk=None):
        compte = self.get_object()
        # Utiliser JournalItem qui est lié au compte
        ecritures = JournalItem.objects.filter(account=compte)
        serializer = JournalItemSerializer(ecritures, many=True)
        return Response(serializer.data)


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)   # <-- ici tu verras le détail
            return Response(serializer.errors, status=400)

# produits
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# factures
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    # exemple : filtrer par partenaire
    def get_queryset(self):
        queryset = super().get_queryset()
        partner_id = self.request.query_params.get('partner')
        if partner_id:
            queryset = queryset.filter(partner_id=partner_id)
        return queryset


# commandes
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['order']

    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')  # récupère order_id depuis la query string
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset

    def perform_create(self, serializer):
        order = serializer.save()
        partner = order.partner

        # Compte du client
        account_client = Account.objects.filter(partner=partner, account_type='asset_receivable').first()
        if not account_client:
            account_client = Account.objects.create(
                name=f"Client {partner.name}",
                account_type="asset_receivable",
                partner=partner
            )

        # Compte Ventes
        account_sales = Account.objects.filter(account_type='income', name='Ventes').first()
        if not account_sales:
            account_sales = Account.objects.create(
                name="Ventes",
                account_type="income"
            )

        # Compte Caisse ou Banque (si paiement direct)
        account_cash = Account.objects.filter(account_type='asset_cash', name='Caisse').first()
        if not account_cash:
            account_cash = Account.objects.create(
                name="Caisse",
                account_type="asset_cash"
            )

        # Créer l'écriture comptable du montant total de la commande
        journal = Journal.objects.filter(type='sale').first()
        if not journal:
            journal = Journal.objects.create(name='Journal des ventes', type='sale')

        entry = JournalEntry.objects.create(
            journal=journal,
            reference=f"COM-{order.id}",
            date=order.date
        )

        # Débit : client
        JournalItem.objects.create(
            entry=entry,
            account=account_client,
            debit=order.total_amount,
            credit=0,
            label=f"Commande {order.id} - {partner.name}"
        )

        # Crédit : ventes
        JournalItem.objects.create(
            entry=entry,
            account=account_sales,
            debit=0,
            credit=order.total_amount,
            label=f"Vente {order.id}"
        )


# éléments de commande
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset

# paiements
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ['pattern']

    def get_queryset(self):
        queryset = super().get_queryset()
        pattern_id = self.request.query_params.get('pattern')
        if pattern_id:
            queryset = queryset.filter(pattern_id=pattern_id)
        return queryset

    def perform_create(self, serializer):
        payment = serializer.save()
        partner = payment.pattern  # le client associé

        # Vérifier que le compte du client existe
        account_partner = Account.objects.filter(partner=partner, account_type='asset_receivable').first()
        if not account_partner:
            raise serializers.ValidationError(
                f"Le compte comptable du client {partner.name} n'existe pas. Créez d'abord la commande."
            )

        # Mapping des modes de paiement vers comptes et journaux
        PAYMENT_MAPPING = {
            'cash': {'account_name': 'Caisse', 'journal_type': 'cash'},
            'bank': {'account_name': 'Banque', 'journal_type': 'bank'},
            'card': {'account_name': 'Banque', 'journal_type': 'bank'},
            'mvola': {'account_name': 'MVola', 'journal_type': 'cash'},
            'orange': {'account_name': 'Orange Money', 'journal_type': 'cash'},
            'airtel': {'account_name': 'Airtel Money', 'journal_type': 'cash'},
            'cod': {'account_name': None, 'journal_type': None},  # paiement à la livraison
        }

        mode = payment.mode.lower()
        if mode not in PAYMENT_MAPPING:
            raise serializers.ValidationError("Mode de paiement non reconnu")

        mapping = PAYMENT_MAPPING[mode]

        # Déterminer le compte à débiter/créditer
        if mode == 'cod':
            account_debit = account_partner
            journal = None
        else:
            account_debit = Account.objects.filter(account_type='asset_cash', name=mapping['account_name']).first()
            if not account_debit:
                raise serializers.ValidationError(
                    f"Le compte '{mapping['account_name']}' n'existe pas. Créez-le d'abord."
                )

            # Journal associé
            journal = Journal.objects.filter(type=mapping['journal_type']).first()
            if not journal:
                raise serializers.ValidationError(
                    f"Aucun journal de type '{mapping['journal_type']}' n'existe. Créez-le d'abord."
                )

        # Créer l'écriture comptable si ce n'est pas cod
        if journal:
            entry = JournalEntry.objects.create(
                journal=journal,
                reference=f"PAY-{payment.id}",
                date=payment.date
            )

            # Débit : compte caisse / banque / mobile money
            JournalItem.objects.create(
                entry=entry,
                account=account_debit,
                debit=payment.amount,
                credit=0,
                label=f"Paiement {payment.id}"
            )

            # Crédit : compte client
            JournalItem.objects.create(
                entry=entry,
                account=account_partner,
                debit=0,
                credit=payment.amount,
                label=f"Paiement reçu de {partner.name}"
            )
        else:
            # Pour COD, pas de journal, juste crédit client
            pass


class PartnerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Partner.objects.all()
        account_type = self.forwarded.get('account_type', None)

        if account_type == 'asset_receivable':
            qs = qs.filter(is_client=True)
        elif account_type == 'liability_payable':
            qs = qs.filter(is_supplier=True)
        else:
            qs = Partner.objects.none()
        return qs

class GeneralLedgerView(APIView):
    def get(self, request):
        # Filtrer par période si fournie
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        entries = JournalItem.objects.all()
        if start_date:
            entries = entries.filter(entry__date__gte=start_date)
        if end_date:
            entries = entries.filter(entry__date__lte=end_date)

        # Regrouper par compte
        ledger = {}
        for item in entries:
            acc = item.account.name
            if acc not in ledger:
                ledger[acc] = {"debit": 0, "credit": 0, "entries": []}
            ledger[acc]["debit"] += item.debit
            ledger[acc]["credit"] += item.credit
            ledger[acc]["entries"].append({
                "date": item.entry.date,
                "journal": item.entry.journal.name,
                "ref": item.entry.reference,
                "debit": item.debit,
                "credit": item.credit,
                "label": item.label
            })

        return Response(ledger)

class TrialBalanceByTypeView(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        items = JournalItem.objects.all()
        if start_date:
            items = items.filter(entry__date__gte=start_date)
        if end_date:
            items = items.filter(entry__date__lte=end_date)

        # Organiser les comptes par type
        account_types = {
            "Assets": ["asset_cash", "asset_receivable", "asset_other"],
            "Liabilities": ["liability_payable", "liability_other"],
            "Income": ["income"],
            "Expenses": ["expense"]
        }

        balance_by_type = {}
        grand_total_debit = 0
        grand_total_credit = 0

        for type_name, type_keys in account_types.items():
            balance_by_type[type_name] = []
            for acc in Account.objects.filter(account_type__in=type_keys):
                debit = items.filter(account=acc).aggregate(Sum('debit'))['debit__sum'] or 0
                credit = items.filter(account=acc).aggregate(Sum('credit'))['credit__sum'] or 0
                balance_by_type[type_name].append({
                    "code": acc.code,
                    "name": acc.name,
                    "debit": debit,
                    "credit": credit,
                    "balance": debit - credit
                })
                grand_total_debit += debit
                grand_total_credit += credit

        return Response({
            "balance_by_type": balance_by_type,
            "grand_total_debit": grand_total_debit,
            "grand_total_credit": grand_total_credit,
            "is_balanced": grand_total_debit == grand_total_credit
        })