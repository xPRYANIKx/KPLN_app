function selectedApprovalSum(rowId) {
    paymentApprovalRecalcCards();
    var paymentSelectedRows = document.getElementById('selectedRows-' + rowId).checked;
    var status_id = document.getElementById('status_id-' + rowId);
    var paymentFullStatus = document.getElementById('paymentFullStatus-' + rowId).checked;
    var a_m_v = document.getElementById('card_available_money_value').innerHTML;

    a_m_v = parseFloat(a_m_v.replace(',', '.'));

    parseFloat(a_m_v)? a_m_v = parseFloat(a_m_v): a_m_v=0;

    if (!paymentSelectedRows) {
        document.getElementById('row-' + rowId).style.background="white";
    }
    else {
        if (a_m_v < 0) {
            document.getElementById('card_selected_for_approval_value').style.color="red";
            document.getElementById('card_available_money_value').style.color="red";
             if (paymentSelectedRows) {
                if (status_id &&  status_id != 'Реком.' && status_id != 'Черновик') {
                    document.getElementById('row-' + rowId).style.background="grey";
                }
                else if (!status_id || status_id == 'Реком.' || status_id == 'Черновик') {
                    document.getElementById('row-' + rowId).style.background="red";
                }
             }
        }
        else {
            document.getElementById('card_selected_for_approval_value').style.color="#34a853";
            document.getElementById('card_available_money_value').style.color="black";
            if (paymentSelectedRows) {
                if (!status_id || status_id == 'Реком.' || status_id == 'Черновик') {
                    if (paymentFullStatus) {
                        document.getElementById('row-' + rowId).style.background="#61e283";
                    }
                    else if (!paymentFullStatus){
                        document.getElementById('row-' + rowId).style.background="#34a853";
                    }
                }
                else {
                    document.getElementById('row-' + rowId).style.background="grey";
                }
            }
        }
    }
}
