"""
URL configuration for comptabiliter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import RedirectView
# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .admin import PartnerAutocomplete
from .views import (
    CurrencyViewSet, TaxViewSet, AccountTagViewSet,  # Suppression de AccountViewSet
    JournalViewSet, JournalEntryViewSet, JournalItemViewSet,
    CompanyViewSet, UserViewSet, TrialBalanceByTypeView, GeneralLedgerView,
    UserDetailView, CompteComptableViewSet, PartnerViewSet,
    CurrentUserView, OrderViewSet, OrderItemViewSet, ProductViewSet, PaymentViewSet,
    InvoiceViewSet, CategoryViewSet, InvoiceItemViewSet  # Ajout de CurrentUserView
)
from django.contrib import admin

router = DefaultRouter()


router.register(r'currencies', CurrencyViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'taxes', TaxViewSet)
router.register(r'account-tags', AccountTagViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'products', ProductViewSet)
router.register(r'comptes', CompteComptableViewSet, basename='compte')
router.register(r'journals', JournalViewSet)
router.register(r'journal-entries', JournalEntryViewSet)
router.register(r'journal-items', JournalItemViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'users', UserViewSet)
router.register(r'partners', PartnerViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'invoice-items', InvoiceItemViewSet)
urlpatterns = [
    path('', RedirectView.as_view(url='http://localhost:5173/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/invoice/', views.create_invoice, name='create_invoice'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', UserDetailView.as_view(), name='user_detail'),
    path('api/trial-balance-by-type/', TrialBalanceByTypeView.as_view(), name='trial-balance-by-type'),
    path('api/general-ledger/', GeneralLedgerView.as_view(), name='general-ledger'),
    path('api/current-user/', CurrentUserView.as_view(), name='current_user'),
    path('partner-autocomplete/', PartnerAutocomplete.as_view(), name='partner-autocomplete'),
    path("ai/", include("ai_assistant.urls")),
]

