from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from dal import autocomplete
from .models import (
    User, Currency, Tax, AccountTag, Account, Journal, JournalEntry, JournalItem,
    Company, Partner, Order, OrderItem, Product, Category, Payment,Invoice, InvoiceItem
)
class MyAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('comptabiliter/css/admin_custom.css',)
        }
admin.site.site_header = "Comptabilité Admin"
admin.site.site_title = "Administration Comptabiliter"
admin.site.index_title = "Bienvenue dans l'administration"

# ==== User Admin personnalisé ====
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

admin.site.register(User, UserAdmin)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ('total_price',)

# Personnalisation de l’affichage des factures
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'partner', 'date', 'due_date', 'amount', 'status', 'tax')
    list_filter = ('status', 'date', 'due_date', 'partner')
    search_fields = ('invoice_number', 'partner__name')
    inlines = [InvoiceItemInline]

# Pour gérer les items seuls
@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'invoice', 'quantity', 'unit_price', 'total_price')
    search_fields = ('product_name', 'invoice__invoice_number')
    list_filter = ('invoice',)



# ==== Currency Admin ====
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')
    search_fields = ('code', 'name', 'symbol')
    ordering = ('code',)
    list_filter = ('symbol',)


# ==== Tax Admin ====
@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')
    search_fields = ('name',)
    list_filter = ('rate',)


# ==== AccountTag Admin ====
@admin.register(AccountTag)
class AccountTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ==== Company Admin ====
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency')
    search_fields = ('name',)
    list_filter = ('currency',)
    autocomplete_fields = ('currency',)

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        js = ('comptabiliter/js/partner_currency.js',)
        widgets = {
            'partner': autocomplete.ModelSelect2(url='partner-autocomplete',forward=['account_type']), 'currency':forms.Select(),
        }

# ==== Account Admin ====
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    form = AccountForm
    list_display = ('code', 'name', 'account_type', 'partner', 'currency', 'reconcile')
    list_filter = ('account_type', 'currency', 'reconcile')
    search_fields = ('code', 'name', 'partner__name')
    readonly_fields = ('code',)
    autocomplete_fields = ('partner', 'currency', 'taxes', 'tags')
    fields = ("code", "name", "account_type", "currency", "partner", "reconcile", "note", "taxes", "tags")


# ==== Partner Admin ====
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_client', 'is_supplier', 'company')
    list_filter = ('type', 'is_client', 'is_supplier', 'company')
    search_fields = ('name', 'email', 'phone', 'mobile')
    autocomplete_fields = ('company',)
    ordering = ('name',)

# ==== JournalItem inline pour JournalEntry ====
class JournalItemInline(admin.TabularInline):
    model = JournalItem
    extra = 1
    fields = ('account', 'label', 'debit', 'credit', 'currency')
    autocomplete_fields = ('account', 'currency')


# ==== JournalEntry Admin avec inline ====
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('reference', 'journal', 'date', 'posted')
    list_filter = ('journal', 'posted', 'date')
    search_fields = ('reference', 'journal__name')
    inlines = [JournalItemInline]
    autocomplete_fields = ('journal',)
    ordering = ('-date',)

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'type')
    search_fields = ('code', 'name')
    list_filter = ('type',)
    ordering = ('code',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ('product',)
    fields = ('product', 'quantity')

# Admin pour les commandes
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'partner', 'status', 'date', 'due_date')
    list_filter = ('status', 'date', 'due_date')
    search_fields = ('partner__name', 'id')
    inlines = [OrderItemInline]
    autocomplete_fields = ('partner',)
    ordering = ('-date',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__id', 'product__name')
    autocomplete_fields = ('order', 'product')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit_price', 'quantity')
    search_fields = ('name',)
    autocomplete_fields = ('category',)
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
    def get_result_label(self, item):
        return item.name

    def get_result_value(self, item):
        # renvoyer l’ID pour Select2
        return item.pk

    def get_results(self, context):
        # optionnel: renvoyer currency avec l’objet
        results = super().get_results(context)
        for r in results:
            partner = Partner.objects.get(pk=r['id'])
            currency_id = partner.company.currency.id if partner.company and partner.company.currency else ''
            r['currency'] = currency_id
        return results
    def get_queryset(self):
        qs = Partner.objects.all().order_by('name')  # <- trier par nom
        account_type = self.forwarded.get('account_type', None)

        if account_type == 'asset_receivable':
            qs = qs.filter(is_client=True)
        elif account_type == 'liability_payable':
            qs = qs.filter(is_supplier=True)
        else:
            qs = Partner.objects.none()
        return qs

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'type', 'mode', 'amount', 'date', 'pattern')
    list_filter = ('type', 'mode', 'date')
    search_fields = ('payment_number', 'description', 'pattern__name')  # recherche sur partner
    ordering = ('-date',)