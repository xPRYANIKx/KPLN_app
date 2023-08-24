function paymentApprovalRecalcCards(page='') {
    var s_f_a_p = document.getElementById('card_selected_for_approval_value').dataset.value;
    var a_m_v = document.getElementById('card_available_money_value').dataset.value;

    var selectedRows = document.getElementsByName('selectedRows');
    var approval_sum = document.getElementsByName('approval_sum');
    var amount = document.getElementsByName('amount');
    var status = document.getElementsByName('status_id');

    s_f_a_p? s_f_a_p = parseFloat(s_f_a_p.replace(',', '.')): s_f_a_p=0;
    a_m_v? a_m_v = parseFloat(parseFloat(a_m_v.replace(',', '.'))): a_m_v=0;

    for (var i=0; i<amount.length; i++) {
        if (selectedRows[i].checked) {
            if (!status.length || status[i].value == 'Черновик' || status[i].value == 'Реком.') {
                var amount_sum = 0;
                amount[i].value? amount_sum = parseFloat(amount[i].value): amount_sum = parseFloat(approval_sum[i].value);

                s_f_a_p = Number((s_f_a_p + amount_sum).toFixed(2));
                a_m_v = Number((a_m_v - amount_sum).toFixed(2));
            }
        }
    }

    if (s_f_a_p == 0) {
        s_f_a_p = '&nbsp;'
    }
    else {
        s_f_a_p += ' ₽'
    }

    if (a_m_v == 0) {
        a_m_v = '&nbsp;'
    }
    else {
        a_m_v += ' ₽'
    }



    document.getElementById('card_selected_for_approval_value').innerHTML = s_f_a_p
    document.getElementById('card_available_money_value').innerHTML = a_m_v


}