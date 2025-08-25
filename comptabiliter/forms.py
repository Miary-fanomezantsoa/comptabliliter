from django import forms
from .models import Account

from .models import JournalEntry, JournalItem
from django.forms.models import inlineformset_factory

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'name', 'code', 'account_type', 'currency', 'reconcile', 'note', 'taxes', 'tags'
        ]
        widgets = {
            'taxes': forms.CheckboxSelectMultiple,
            'tags': forms.CheckboxSelectMultiple,
            'note': forms.Textarea(attrs={'rows': 3}),
        }
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['date', 'journal', 'reference', 'posted']

JournalItemFormSet = inlineformset_factory(
    JournalEntry, JournalItem,
    fields=['account', 'label', 'debit', 'credit', 'currency'],
    extra=2,
    can_delete=False
)