document.addEventListener('DOMContentLoaded', function() {
    const partnerField = document.querySelector('#id_partner');
    const currencyField = document.querySelector('#id_currency');

    if (partnerField) {
        partnerField.addEventListener('change', function() {
            const selectedOption = partnerField.selectedOptions[0];
            const data = $(partnerField).select2('data')[0];
            if (data && data.currency) {
                currencyField.value = data.currency;  // met automatiquement la currency
            }
        });
    }
});
