from datetime import date
from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError


# ==== Utilisateur ====
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin_comptable', 'Responsable Comptable Admin'),
        ('comptable', 'Comptable'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='comptable')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# ==== Paramètres Comptables ====
class Currency(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=8)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f"{self.code} - {self.symbol}"


class Tax(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class AccountTag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name





# ==== Journaux ====
class Journal(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=32, choices=[
        ('bank', 'Bank'),
        ('cash', 'Cash'),
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('general', 'General'),
    ])

    def __str__(self):
        return f"{self.code} - {self.name}"


class JournalEntry(models.Model):
    date = models.DateField()
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    reference = models.CharField(max_length=64, blank=True)
    posted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reference or 'Entry'} - {self.date}"





# ==== Entreprises ====
class Company(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"


class Partner(models.Model):
    PARTNER_TYPE = [
        ('person', 'Personne'),
        ('company', 'Entreprise'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=PARTNER_TYPE, default='person')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Rôles comme dans Odoo : client / fournisseur
    is_client = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

    company = models.ForeignKey("Company", on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.name} ({'Client' if self.is_client else 'Fournisseur'})"

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('asset_receivable', 'Asset Receivable'),
        # Actif à recevoir : ce sont les créances que l’entreprise doit recevoir, généralement des clients.
        # Exemple : factures clients non encore payées.

        ('asset_cash', 'Cash'),
        # Actif liquide : l’argent en caisse ou en banque.
        # Exemple : caisse, comptes bancaires.

        ('liability_payable', 'Liability Payable'),
        # Passif à payer : dettes ou obligations de l’entreprise envers des tiers.
        # Exemple : fournisseurs, dettes fiscales ou sociales.

        ('equity', 'Equity'),
        # Capitaux propres : fonds apportés par les propriétaires ou les bénéfices accumulés.
        # Exemple : capital social, réserves, résultat reporté.

        ('income', 'Income'),
        # Produits / Revenus : ce que l’entreprise gagne.
        # Exemple : ventes de produits, prestations de services, revenus financiers.

        ('expense', 'Expense'),
        # Charges / Dépenses : ce que l’entreprise dépense pour son fonctionnement.
        # Exemple : achats de marchandises, salaires, loyers, frais financiers.
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    account_type = models.CharField(max_length=32, choices=ACCOUNT_TYPES)
    currency = models.ForeignKey("Currency", null=True, blank=True, on_delete=models.SET_NULL)
    reconcile = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    taxes = models.ManyToManyField("Tax", blank=True)
    tags = models.ManyToManyField("AccountTag", blank=True)
    partner = models.ForeignKey(Partner, null=True, blank=True, on_delete=models.SET_NULL)
    classe = models.CharField(max_length=1, blank=True, null=True)
    sous_classe = models.CharField(max_length=2, blank=True, null=True)
    compte=models.CharField(max_length=3, blank=True, null=True)
    sous_compte=models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def clean(self):
        #"""Validation des contraintes entre type de compte et partenaire"""
        if self.account_type == 'asset_receivable':
            if not self.partner or not self.partner.is_client:
                raise ValidationError("Un compte 'Asset Receivable' doit être lié à un partenaire de type Client.")

        if self.account_type == 'liability_payable':
            if not self.partner or not self.partner.is_supplier:
                raise ValidationError("Un compte 'Liability Payable' doit être lié à un partenaire de type Fournisseur.")

        if self.account_type == 'asset_cash' and self.partner:
            raise ValidationError("Un compte 'Cash' ne doit pas avoir de partenaire.")

        if self.account_type == 'equity' and self.partner:
            raise ValidationError("Un compte 'Equity' ne doit pas avoir de partenaire.")

    def save(self, *args, **kwargs):
        #"""Génération automatique du code AAAAXXXX"""
        if not self.code:
            current_year = date.today().year
            last_compte = Account.objects.filter(code__startswith=str(current_year)).order_by('code').last()
            if last_compte:
                last_number = int(last_compte.code[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.code = f"{current_year}{new_number:04d}"
        super().save(*args, **kwargs)
class JournalItem(models.Model):
    entry = models.ForeignKey(JournalEntry, related_name='lines', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    label = models.CharField(max_length=128, blank=True)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.account} | Dr: {self.debit} / Cr: {self.credit}"


class HistoriqueModification(models.Model):
    compte = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="historiques")
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    date_action = models.DateTimeField(auto_now_add=True)
    ancienne_valeur = models.TextField(blank=True, null=True)
    nouvelle_valeur = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} - {self.compte.code}"


# Modèle pour les catégories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Modèle produit
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='unpaid')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)

    def __str__(self):
        return f"Facture #{self.invoice_number} - {self.partner.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.unit_price


class Order(models.Model):
    date = models.DateField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')

    def __str__(self):
        return f"Order #{self.id} - {self.partner.name} - {self.status}"

    @property
    def total_amount(self):
        return sum(item.quantity * item.product.unit_price for item in self.orderitem_set.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) for Order #{self.order.id}"

class Payment(models.Model):
    payment_number = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    mode = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pattern = models.ForeignKey(Partner, on_delete=models.CASCADE)
    def __str__(self):
        return f"Payment #{self.payment_number}"

class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    type = models.CharField(max_length=50, default='info')
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type.upper()}: {self.message[:50]}"
