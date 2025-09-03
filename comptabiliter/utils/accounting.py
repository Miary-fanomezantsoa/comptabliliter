from ..models import Account

ACCOUNT_RULES = {
    "asset_receivable": {"classe": "4", "sous_classe": "41", "compte": "411"},
    "liability_payable": {"classe": "4", "sous_classe": "40", "compte": "401"},
    "asset_cash": {"classe": "5", "sous_classe": "51", "compte": "512"},
    "income": {"classe": "7", "sous_classe": "70", "compte": "707"},
    "expense": {"classe": "6", "sous_classe": "60", "compte": "601"},
    "equity": {"classe": "1", "sous_classe": "10", "compte": "101"},
}

def get_or_create_account(partner, account_type, label=None):
    rules = ACCOUNT_RULES.get(account_type)
    if not rules:
        raise ValueError(f"Aucune règle comptable définie pour {account_type}")

    qs = Account.objects.filter(account_type=account_type)
    if partner:
        qs = qs.filter(partner=partner)

    account = qs.first()
    if account:
        return account

    base_compte = rules["compte"]
    if partner:
        sous_compte = f"{base_compte}{partner.id:03d}"
    else:
        sous_compte = base_compte

    account = Account.objects.create(
        name=label or f"{partner.name if partner else ''} {rules['compte']}",
        account_type=account_type,
        partner=partner,
        classe=rules["classe"],
        sous_classe=rules["sous_classe"],
        compte=rules["compte"],
        sous_compte=sous_compte,
        code=sous_compte
    )
    return account
