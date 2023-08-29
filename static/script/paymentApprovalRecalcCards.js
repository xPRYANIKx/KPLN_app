function paymentApprovalRecalcCards() {
    var s_f_a_p = document.getElementById('card_selected_for_approval_value').dataset.value;
    var a_m_v = document.getElementById('card_available_money_value').dataset.value;

    var selectedRows = document.getElementsByName('selectedRows');
    var approvalSum = document.getElementsByName('approval_sum');
    var amount = document.getElementsByName('amount');
    var statusId = document.getElementsByName('status_id');

    s_f_a_p? s_f_a_p = parseFloat(s_f_a_p.replace(',', '.')).toFixed(2): s_f_a_p=0;
    a_m_v? a_m_v = parseFloat(a_m_v.replace(',', '.')).toFixed(2): a_m_v=0;

    for (var i=0; i<amount.length; i++) {
        if (selectedRows[i].checked) {
            if (!statusId.length || statusId[i].value == 'Черновик' || statusId[i].value == 'Реком.') {
                var amount_sum = 0;

                amount[i].value = amount[i].value.replace('₽', '').replace(' руб.', '').replace(/ /g, "").replace(",", ".")

                amount[i].value? amount_sum = parseFloat(amount[i].value): amount_sum = 0;
                amount_sum > parseFloat(approvalSum[i].value)? amount_sum=parseFloat(approvalSum[i].value) : 0;
                amount_sum < 0 ? amount_sum = 0 : 0;

                parseFloat(a_m_v) < amount_sum ? amount_sum=a_m_v : 0;

                s_f_a_p = (parseFloat(s_f_a_p) + amount_sum).toFixed(2);

                a_m_v = (parseFloat(a_m_v) - amount_sum).toFixed(2);
            }
        }
        tabColorize(i);
    }

    if (s_f_a_p == 0) {
        s_f_a_p = '0 ₽'
    }
    else {
        s_f_a_p += ' ₽'
    }

    if (a_m_v == 0) {
        a_m_v = '0 ₽'
    }
    else {
        a_m_v += ' ₽'
    }

    document.getElementById('card_selected_for_approval_value').innerHTML = s_f_a_p
    document.getElementById('card_available_money_value').innerHTML = a_m_v
}
