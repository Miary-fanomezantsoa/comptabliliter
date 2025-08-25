from dal import autocomplete
from django.db.models import Sum
from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
import json
from django.http import HttpResponse
import pandas as pd
from datetime import datetime
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
        partner = payment.pattern  # correct

        # Compte partenaire
        account_partner = Account.objects.filter(partner=partner, account_type='asset_receivable').first()
        if not account_partner:
            account_partner = Account.objects.create(
                name=f"Client {partner.name}",
                account_type="asset_receivable",
                partner=partner
            )

        # Compte Banque ou Caisse
        if payment.mode in ['cash', 'cheque', 'transfer']:
            account_cash = Account.objects.filter(account_type='asset_cash', name='Banque').first()
            if not account_cash:
                account_cash = Account.objects.create(
                    name='Banque',
                    account_type='asset_cash'
                )

        # Journal de paiement
        journal = Journal.objects.filter(type='cash').first()
        if not journal:
            journal = Journal.objects.create(name='Journal de caisse', type='cash')

        entry = JournalEntry.objects.create(
            journal=journal,
            reference=f"PAY-{payment.id}",
            date=payment.date
        )

        # Débit : banque / caisse
        JournalItem.objects.create(
            entry=entry,
            account=account_cash,
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


