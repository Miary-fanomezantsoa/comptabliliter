import io
import logging
import os
from ai_assistant.services.gemini import ask_gemini
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib import colors, logger
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from dal import autocomplete
from django.db.models import Sum, Max
from django.http import HttpResponse, JsonResponse
from reportlab.platypus import Table, TableStyle
from rest_framework import viewsets, filters, serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
import json
from .models import (
    Currency, Tax, AccountTag, Account,
    Journal, JournalEntry, JournalItem, Partner,
    Company, HistoriqueModification, Order, Invoice, Product, OrderItem, Payment, User, Category,
    InvoiceItem, Notification
)
from .serializers import (
    CurrencySerializer, TaxSerializer, AccountTagSerializer, AccountSerializer,
    JournalSerializer, JournalEntrySerializer, JournalItemSerializer, PartnerSerializer,
    CompanySerializer, UserSerializer,
    HistoriqueModificationSerializer, SafeUserSerializer, PaymentSerializer, OrderItemSerializer, OrderSerializer,
    InvoiceSerializer, ProductSerializer, CategorySerializer, InvoiceItemSerializer
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
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_superuser:
            return Response({"detail": "Impossible de supprimer le super utilisateur."}, status=403)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_superuser and 'role' in request.data:
            request.data['role'] = user.role
        return super().update(request, *args, **kwargs)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
    serializer_class = AccountSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name']
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
        ancienne = AccountSerializer(instance).data
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
            ancienne_valeur=json.dumps(AccountSerializer(instance).data)
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

    # Filtrer par client (partner)
    def get_queryset(self):
        queryset = super().get_queryset()
        partner_id = self.request.query_params.get("partner")
        if partner_id:
            queryset = queryset.filter(partner_id=partner_id)
        return queryset

    # ✅ Endpoint personnalisé : /api/invoice/{id}/generate_pdf/
    @action(detail=True, methods=["get"])
    def generate_pdf(self, request, pk=None):
        try:
            # On récupère la commande
            order = Order.objects.get(pk=pk)
            items = OrderItem.objects.filter(order=order)
            partner = order.partner

            # === 1️⃣ Vérifier si la facture existe déjà ===
            invoice, created = Invoice.objects.get_or_create(
                partner=partner,
                invoice_number=f"INV-{order.id}",
                defaults={
                    "date": timezone.now().date(),
                    "due_date": timezone.now().date() + timezone.timedelta(days=30),
                    "amount": sum(i.quantity * i.product.unit_price for i in items),
                    "status": "unpaid",
                }
            )

            # === 2️⃣ Créer les lignes de facture si c’est une nouvelle facture ===
            if created:
                for i in items:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product_name=i.product.name,
                        quantity=i.quantity,
                        unit_price=i.product.unit_price
                    )

            # === 3️⃣ Générer le PDF ===
            buffer = generate_invoice_pdf(invoice, [
                {
                    "name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price)
                } for item in invoice.items.all()
            ], logo_path="static/logo.png")

            response = HttpResponse(buffer, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="facture_{invoice.invoice_number}.pdf"'
            return response

        except Order.DoesNotExist:
            return Response({"error": "Commande introuvable"}, status=status.HTTP_404_NOT_FOUND)

# =========================
#   VIEWSET DES LIGNES DE FACTURES
# =========================
class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer


# =========================
#   VIEW CLASSIQUE (optionnelle)
# =========================
@csrf_exempt
def create_invoice(request):
    """Créer une facture et l'exporter en PDF"""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    order_id = data.get("order_id")
    export_pdf = data.get("export_pdf", False)

    try:
        order = Order.objects.get(id=order_id)
        items = OrderItem.objects.filter(order=order)
        partner = order.partner

        # === Création ou récupération de la facture ===
        invoice, created = Invoice.objects.get_or_create(
            partner=partner,
            invoice_number=f"INV-{order.id}",
            defaults={
                "date": timezone.now().date(),
                "due_date": timezone.now().date() + timezone.timedelta(days=30),
                "amount": sum(i.quantity * i.product.unit_price for i in items),
                "status": "unpaid",
            }
        )

        # === Création des lignes si c'est une nouvelle facture ===
        if created:
            for i in items:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product_name=i.product.name,
                    quantity=i.quantity,
                    unit_price=i.product.unit_price
                )

        if export_pdf:
            # Passer l'objet Invoice à generate_invoice_pdf
            buffer = generate_invoice_pdf(invoice)
            response = HttpResponse(buffer, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="facture_{invoice.invoice_number}.pdf"'
            return response
        else:
            # Retour JSON
            return JsonResponse({
                "invoice_number": invoice.invoice_number,
                "date": invoice.date.strftime('%d/%m/%Y'),
                "client": partner.name,
                "items": [{"product": i.product_name, "quantity": i.quantity, "unit_price": float(i.unit_price)} for i in invoice.items.all()],
                "total": float(invoice.amount),
                "status": invoice.status
            })

    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

# =========================
#   FONCTION DE GÉNÉRATION PDF
# =========================
# === CONFIG LOGGING ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === FONCTION DE GÉNÉRATION PDF ===
def generate_invoice_pdf(invoice, items=None, logo_path=None):
    """
    Génère un PDF de facture à partir d'un objet Invoice.

    :param invoice: Invoice instance
    :param items: Optionnel, liste de dictionnaires {"name", "quantity", "unit_price"}.
                  Si None, prend les InvoiceItem liés à la facture.
    :param logo_path: Chemin du logo, sinon chemin par défaut
    :return: io.BytesIO contenant le PDF
    """
    if logo_path is None:
        logo_path = os.path.join(settings.BASE_DIR, "comptabiliter/static/logo.png")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # === LOGO ===
    logo_width = 4 * cm
    logo_height = 4 * cm
    x = width - logo_width - 2 * cm
    y = height - logo_height - 2 * cm

    if logo_path and os.path.exists(logo_path):
        try:
            p.drawImage(logo_path, x, y, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            logger.error(f"Erreur lors du dessin du logo : {e}")
    else:
        logger.warning(f"Logo non trouvé : {logo_path}")

    # === TITRE ===
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 2 * cm, "FACTURE")

    # === INFOS FACTURE ===
    p.setFont("Helvetica", 12)
    y_info = height - 5 * cm
    p.drawString(2 * cm, y_info, f"Facture n° : {invoice.invoice_number}")
    p.drawString(2 * cm, y_info - 1 * cm, f"Client : {invoice.partner.name}")
    p.drawString(2 * cm, y_info - 2 * cm, f"Date : {invoice.date.strftime('%d/%m/%Y')}")
    p.drawString(2 * cm, y_info - 3 * cm, f"État : {invoice.status}")

    # === TABLEAU DES PRODUITS ===
    if items is None:
        items = [
            {"name": i.product_name, "quantity": i.quantity, "unit_price": float(i.unit_price)}
            for i in invoice.items.all()
        ]

    table_data = [["Produit", "Quantité", "Prix unitaire", "Total"]]
    total_general = 0
    for item in items:
        total_ligne = item["quantity"] * item["unit_price"]
        total_general += total_ligne
        table_data.append([
            item["name"],
            str(item["quantity"]),
            f"{item['unit_price']:.2f}",
            f"{total_ligne:.2f}"
        ])

    # === PAIEMENTS ===
    payments = Payment.objects.filter(pattern=invoice.partner, date__lte=invoice.date)
    total_paid = sum(p.amount for p in payments)
    reste_a_payer = invoice.amount - total_paid

    table_data.append(["", "", "TOTAL", f"{total_general:.2f}"])
    table_data.append(["", "", "Total payé", f"{total_paid:.2f}"])
    table_data.append(["", "", "Reste à payer", f"{reste_a_payer:.2f}"])

    table = Table(table_data, colWidths=[7 * cm, 3 * cm, 3 * cm, 3 * cm])
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ])
    table.setStyle(style)
    table.wrapOn(p, width, height)
    table.drawOn(p, 2 * cm, y_info - 8 * cm)

    # === PIED DE PAGE ===
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width / 2, 1.5 * cm, "Merci pour votre achat ✨")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
# === VUE DJANGO POUR RENVOYER LE PDF ===
def invoice_view(request, order_id):
    order = Order.objects.get(id=order_id)
    items = [
        {"name": i.product.name, "quantity": i.quantity, "unit_price": i.unit_price}
        for i in order.items.all()
    ]
    pdf_buffer = generate_invoice_pdf(order, items)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="facture_{order.id}.pdf"'
    return response


# commandes
# Fonction utilitaire pour déterminer la classe, sous-classe, compte et sous-compte
def get_account_structure(account_type):
    """
    Retourne un dict avec classe, sous_classe, compte et sous_compte
    selon le type de compte (PCG standard)
    """
    if account_type == "asset_receivable":
        return {"classe":"4", "sous_classe":"10", "compte":"401", "sous_compte":"0001"}  # Client
    elif account_type == "liability_payable":
        return {"classe":"4", "sous_classe":"20", "compte":"401", "sous_compte":"0002"}  # Fournisseur
    elif account_type == "asset_cash":
        return {"classe":"5", "sous_classe":"10", "compte":"512", "sous_compte":"0000"}  # Banque / caisse
    elif account_type == "income":
        return {"classe":"7", "sous_classe":"10", "compte":"701", "sous_compte":"0000"}  # Ventes
    elif account_type == "expense":
        return {"classe":"6", "sous_classe":"10", "compte":"601", "sous_compte":"0000"}  # Achats
    else:
        return {"classe":"0", "sous_classe":"00", "compte":"000", "sous_compte":"0000"}

# --- OrderViewSet ---
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['order']

    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset

    def perform_create(self, serializer):
        order = serializer.save()
        partner = order.partner

        # --- Fonction utilitaire pour créer ou récupérer un compte ---
        def get_or_create_account(partner, account_type, name):
            account = Account.objects.filter(partner=partner, account_type=account_type, name=name).first()
            if not account:
                structure = get_account_structure(account_type)
                account = Account.objects.create(
                    name=name,
                    account_type=account_type,
                    partner=partner,
                    classe=structure["classe"],
                    sous_classe=structure["sous_classe"],
                    compte=structure["compte"],
                    sous_compte=structure["sous_compte"],
                )
            return account

        # --- Création / récupération des comptes ---
        account_client = get_or_create_account(partner, "asset_receivable", f"Client {partner.name}") if getattr(partner, 'is_client', False) else None
        account_supplier = get_or_create_account(partner, "liability_payable", f"Fournisseur {partner.name}") if getattr(partner, 'is_supplier', False) else None
        account_sales = get_or_create_account(None, "income", "Ventes")
        account_purchase = get_or_create_account(None, "expense", "Achats")
        account_cash = get_or_create_account(None, "asset_cash", "Caisse")

        # --- VENTES (si partenaire client) ---
        if account_client:
            journal_sale = Journal.objects.filter(type='sale').first()
            if not journal_sale:
                journal_sale = Journal.objects.create(name='Journal des ventes', type='sale')

            entry_sale = JournalEntry.objects.create(
                journal=journal_sale,
                reference=f"COM-{order.id}",
                date=order.date
            )

            # Débit client
            JournalItem.objects.create(
                entry=entry_sale,
                account=account_client,
                debit=order.total_amount,
                credit=0,
                label=f"Commande {order.id} - {partner.name}"
            )

            # Crédit ventes
            JournalItem.objects.create(
                entry=entry_sale,
                account=account_sales,
                debit=0,
                credit=order.total_amount,
                label=f"Vente {order.id}"
            )

        # --- ACHATS (si partenaire fournisseur) ---
        if account_supplier:
            journal_purchase = Journal.objects.filter(type='purchase').first()
            if not journal_purchase:
                journal_purchase = Journal.objects.create(name='Journal des achats', type='purchase')

            entry_purchase = JournalEntry.objects.create(
                journal=journal_purchase,
                reference=f"ACH-{order.id}",
                date=order.date
            )

            # Débit achats
            JournalItem.objects.create(
                entry=entry_purchase,
                account=account_purchase,
                debit=order.total_amount,
                credit=0,
                label=f"Achat {order.id} - {partner.name}"
            )

            # Crédit fournisseur
            JournalItem.objects.create(
                entry=entry_purchase,
                account=account_supplier,
                debit=0,
                credit=order.total_amount,
                label=f"Dette fournisseur {order.id}"
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

def generate_unique_code(prefix=''):
    year = datetime.date.today().year

    # Récupérer le max des codes pour l'année courante
    last_code = (
        Account.objects
        .filter(code__startswith=str(year))
        .aggregate(max_code=Max('code'))
        .get('max_code')
    )

    if last_code:
        # Extraire la partie numérique après l'année
        last_number = int(last_code[-4:])
        new_number = last_number + 1
    else:
        new_number = 1

    # Formatter : 20250001
    return f"{year}{new_number:04d}"


def get_default_currency():
    # Essaie de récupérer la devise marquée par défaut
    default = Currency.objects.filter(is_default=True).first()
    if default:
        return default

    # Sinon, prend la première devise existante
    currency = Currency.objects.first()
    if currency:
        return currency

    # Si aucune devise n'existe → en créer une
    return Currency.objects.create(
        name="Ariary",
        code="MGA",
        symbol="Ar",
        is_default=True
    )


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

        # Vérifie que le compte du client existe
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
            account_debit = Account.objects.filter(account_type='asset_cash', name='account_name').first()
            journal = None
        else:
            account_name = mapping['account_name']
            account_debit = Account.objects.filter(account_type='asset_cash', name=mapping['account_name']).first()
            if not account_debit:
                # Définir des valeurs différentes selon le type
                if account_name.lower() == 'caisse':
                    code = generate_unique_code(prefix='CA')  # CA pour caisse
                    classe = '1'
                    sous_classe = '01'
                    compte = '101'
                    sous_compte = '0001'
                elif account_name.lower() == 'banque':
                    code = generate_unique_code(prefix='BA')  # BA pour banque
                    classe = '1'
                    sous_classe = '02'
                    compte = '102'
                    sous_compte = '0001'
                else:
                    code = generate_unique_code()
                    classe = '1'
                    sous_classe = '03'
                    compte = '103'
                    sous_compte = '0001'

                # Créer le compte avec toutes les infos
                account_debit = Account.objects.create(
                    name=account_name,
                    account_type='asset_cash',
                    code=code,
                    classe=classe,
                    sous_classe=sous_classe,
                    compte=compte,
                    sous_compte=sous_compte,
                    currency=get_default_currency,  # objet Currency par défaut
                    reconcile=False,
                    note=f"Compte créé automatiquement pour {account_name}"
                )

            # Journal associé
            journal = Journal.objects.filter(type=mapping['journal_type']).first()
            if not journal:
                journal = Journal.objects.create(
                    name=f"Journal {mapping['account_name']}",
                    code=mapping['account_name'][:2].upper(),  # ex: CA pour caisse, BA pour banque
                    type=mapping['journal_type']
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

#filtre les partenaire en fonction de type de compte
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

#grand livre
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

#balance comptable
class TrialBalanceByTypeView(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        items = JournalItem.objects.all()
        if start_date:
            items = items.filter(entry__date__gte=start_date)
        if end_date:
            items = items.filter(entry__date__lte=end_date)

        accounts = Account.objects.all()

        # Ordre prédéfini des comptes par classe pour l'affichage
        order_classe_1_5 = [
            "Capital",
            "Bénéfice reporté",
            "Perte reportée",
            "Machines",
            "Mobilier",
            "Matériel roulant",
            "Clients",
            "Fournisseurs",
            "Banque",
            "Caisse"
        ]

        order_classe_6_7 = [
            "Achats de marchandises",
            "Bénéfice reporté",
            "Perte reportée",
            "Vente de marchandises"
        ]

        balance_by_class = {
            "Classes 1 à 5": {
                "accounts": [],
                "total_debit": 0,
                "total_credit": 0,
                "total_debit_solde": 0,
                "total_credit_solde": 0,
            },
            "Classes 6 et 7": {
                "accounts": [],
                "total_debit": 0,
                "total_credit": 0,
                "total_debit_solde": 0,
                "total_credit_solde": 0,
            }
        }

        grand_total_debit_total = 0
        grand_total_credit_total = 0
        grand_total_debit_solde = 0
        grand_total_credit_solde = 0

        for acc in accounts:
            # Calcul des totaux pour le compte
            debit_total = items.filter(account=acc).aggregate(Sum("debit"))["debit__sum"] or 0
            credit_total = items.filter(account=acc).aggregate(Sum("credit"))["credit__sum"] or 0
            debit_solde = max(0, debit_total - credit_total)
            credit_solde = max(0, credit_total - debit_total)

            account_data = {
                "code": acc.code,
                "name": acc.name,
                "debit_total": debit_total,
                "credit_total": credit_total,
                "debit_solde": debit_solde,
                "credit_solde": credit_solde,
            }

            # Classe 1 à 5
            if acc.code and acc.code[0] in "12345":
                balance_by_class["Classes 1 à 5"]["accounts"].append(account_data)
                balance_by_class["Classes 1 à 5"]["total_debit"] += debit_total
                balance_by_class["Classes 1 à 5"]["total_credit"] += credit_total
                balance_by_class["Classes 1 à 5"]["total_debit_solde"] += debit_solde
                balance_by_class["Classes 1 à 5"]["total_credit_solde"] += credit_solde

            # Classe 6 et 7
            elif acc.code and acc.code[0] in "67":
                balance_by_class["Classes 6 et 7"]["accounts"].append(account_data)
                balance_by_class["Classes 6 et 7"]["total_debit"] += debit_total
                balance_by_class["Classes 6 et 7"]["total_credit"] += credit_total
                balance_by_class["Classes 6 et 7"]["total_debit_solde"] += debit_solde
                balance_by_class["Classes 6 et 7"]["total_credit_solde"] += credit_solde

            # Mise à jour des grands totaux
            grand_total_debit_total += debit_total
            grand_total_credit_total += credit_total
            grand_total_debit_solde += debit_solde
            grand_total_credit_solde += credit_solde

        # Trier les comptes selon l'ordre prédéfini
        def sort_accounts(accounts_list, order_list):
            sorted_list = []
            for name in order_list:
                for acc in accounts_list:
                    if acc["name"] == name:
                        sorted_list.append(acc)
            # Ajouter les comptes restants qui ne sont pas dans l'ordre prédéfini
            for acc in accounts_list:
                if acc not in sorted_list:
                    sorted_list.append(acc)
            return sorted_list

        balance_by_class["Classes 1 à 5"]["accounts"] = sort_accounts(
            balance_by_class["Classes 1 à 5"]["accounts"], order_classe_1_5
        )
        balance_by_class["Classes 6 et 7"]["accounts"] = sort_accounts(
            balance_by_class["Classes 6 et 7"]["accounts"], order_classe_6_7
        )

        return Response({
            "balance_by_type": balance_by_class,
            "grand_total_debit_total": grand_total_debit_total,
            "grand_total_credit_total": grand_total_credit_total,
            "grand_total_debit_solde": grand_total_debit_solde,
            "grand_total_credit_solde": grand_total_credit_solde,
            "is_balanced": grand_total_debit_total == grand_total_credit_total,
        })


#notification
def analyze_database(user):
    """
    Analyse les écritures comptables et les partenaires.
    Ajoute une notification pour chaque problème détecté,
    avec une suggestion IA via Gemini.
    """
    problems_found = False

    # Récupérer toutes les écritures comptables
    entries = JournalEntry.objects.all()

    for entry in entries:
        items = entry.lines.all()  # JournalItem liés à cette écriture
        debit_total = items.aggregate(total=Sum('debit'))['total'] or 0
        credit_total = items.aggregate(total=Sum('credit'))['total'] or 0

        # Vérifier qu'il y a au moins deux lignes
        if items.count() < 2:
            message = f"L'écriture {entry.id} du journal {entry.journal.code} n'a pas assez de lignes (moins de 2)."
            suggestion = ask_gemini(
                f"Que doit faire un comptable si une écriture comptable n'a qu'une seule ligne ? "
                f"Contexte : {message}"
            )
            Notification.objects.create(
                user=user,
                message=message + f"\n💡 Suggestion IA : {suggestion}",
                type='error'
            )
            problems_found = True

        # Vérifier équilibre débit/crédit
        if debit_total != credit_total:
            message = (
                f"L'écriture {entry.id} du journal {entry.journal.code} "
                f"n'est pas équilibrée (Débit={debit_total}, Crédit={credit_total})."
            )
            suggestion = ask_gemini(
                f"Comment corriger une écriture comptable déséquilibrée ? "
                f"Contexte : {message}"
            )
            Notification.objects.create(
                user=user,
                message=message + f"\n💡 Suggestion IA : {suggestion}",
                type='error'
            )
            problems_found = True

        # Vérifier référence vide
        if not entry.reference:
            message = f"L'écriture {entry.id} du journal {entry.journal.code} n'a pas de référence."
            suggestion = ask_gemini(
                f"Pourquoi est-il important d'avoir une référence sur une écriture comptable "
                f"et que doit-on faire si elle est manquante ? "
                f"Contexte : {message}"
            )
            Notification.objects.create(
                user=user,
                message=message + f"\n💡 Suggestion IA : {suggestion}",
                type='warning'
            )
            problems_found = True

    # ==== Analyse des partenaires ====
    partners = Partner.objects.all()
    for partner in partners:
        if not partner.is_client and not partner.is_supplier:
            # Si partenaire ni client ni fournisseur → on ignore
            continue

        accounts = Account.objects.filter(partner=partner)
        if not accounts.exists() and not (partner.is_client and partner.is_supplier):
            message = f"Le partenaire {partner.name} n'a aucun compte comptable associé."
            suggestion = ask_gemini(
                f"Quel compte comptable faut-il associer à un partenaire "
                f"({ 'client' if partner.is_client else 'fournisseur' }) ? "
                f"Contexte : {partner.name}"
            )
            Notification.objects.create(
                user=user,
                message=message + f"\n💡 Suggestion IA : {suggestion}",
                type='error'
            )
            problems_found = True

        elif accounts.count() > 2:
            message = f"Le partenaire {partner.name} possède plus de 2 comptes comptables (actuellement {accounts.count()})."
            suggestion = ask_gemini(
                f"Un partenaire ne doit pas avoir plus de 2 comptes comptables. "
                f"Que doit faire le comptable dans ce cas ? "
                f"Contexte : {partner.name}"
            )
            Notification.objects.create(
                user=user,
                message=message + f"\n💡 Suggestion IA : {suggestion}",
                type='warning'
            )
            problems_found = True

    # ==== Si aucune incohérence trouvée ====
    if not problems_found:
        Notification.objects.create(
            user=user,
            message="✅ Analyse terminée : toutes les écritures comptables et partenaires semblent corrects.",
            type='info'
        )


@api_view(['GET'])
def get_notifications(request):
    """
    Récupère les notifications non lues pour l'utilisateur
    """
    notifications = Notification.objects.filter(user=request.user, read=False).order_by('-created_at')
    data = [{
        "id": n.id,
        "message": n.message,
        "type": n.type,
        "read": n.read,
        "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for n in notifications]
    return Response(data)


@api_view(['POST'])
def run_analysis(request):
    """
    Lance l'analyse de la base pour l'utilisateur connecté
    """
    user = request.user
    analyze_database(user)
    return Response({"message": "Analyse terminée, notifications créées."})
@api_view(['POST'])
def mark_notification_read(request, pk):
    try:
        notif = Notification.objects.get(pk=pk, user=request.user)
        notif.read = True
        notif.save()
        return Response({"message": "Notification marquée comme lue."})
    except Notification.DoesNotExist:
        return Response({"error": "Notification non trouvée."}, status=404)
