function selectedApprovalSum(rowId) {
    var paymentSelectedRows = document.getElementById('selectedRows-' + rowId).checked;
    var paymentApproval_sum = document.getElementById('approvalSum-' + rowId).value;
    var paymentAmount = document.getElementById('amount-' + rowId).value;
    var s_f_a_p = document.getElementById('card_selected_for_approval_value').innerHTML;
    var a_m_v = document.getElementById('card_available_money_value').innerHTML;

    s_f_a_p = parseFloat(s_f_a_p.replace(',', '.'));
    a_m_v = parseFloat(a_m_v.replace(',', '.'));

    parseFloat(s_f_a_p)? s_f_a_p = parseFloat(s_f_a_p): s_f_a_p=0;
    parseFloat(a_m_v)? a_m_v = parseFloat(a_m_v): a_m_v=0;

    paymentAmount? paymentAmount = parseFloat(paymentAmount): paymentAmount = parseFloat(paymentApproval_sum);

    if (paymentSelectedRows) {
        s_f_a_p = (s_f_a_p + paymentAmount).toFixed(2);
        a_m_v = (a_m_v - paymentAmount).toFixed(2);
    }
    else {
        s_f_a_p = (s_f_a_p - paymentAmount).toFixed(2);
        a_m_v = (a_m_v + paymentAmount).toFixed(2);
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
