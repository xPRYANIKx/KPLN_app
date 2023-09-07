$(document).ready(function () {
    tabColorize();
});


function tabColorize(rowId='') {
    if (rowId) {
        var paymentSelectedRows = document.getElementById('selectedRows-' + rowId).checked;
        var approvalSum = document.getElementById('approvalSum-' + rowId).value;
        var amount = document.getElementById('amount-' + rowId).value;
        var statusId = document.getElementById('status_id-' + rowId);
        var paymentFullStatus = document.getElementById('paymentFullStatus-' + rowId).checked;
        var a_m_v = document.getElementById('card_available_money_value').innerHTML;


        a_m_v = parseFloat(a_m_v.replace(',', '.'));

        if (statusId) {
            statusId = statusId.value
        }

        if (a_m_v < 0) {

        }
        else {
            document.getElementById('card_selected_for_approval_value').style.color="#34a853";
            document.getElementById('card_available_money_value').style.color="black";
        }

        if (statusId && statusId !== 'Черновик') {
            document.getElementById('status-' + rowId).style.background="#00000000"
        }

        if (!paymentSelectedRows) {
            document.getElementById('row-' + rowId).style.borderBottom="none";
            rowId%2? document.getElementById('row-' + rowId).style.background="#eaedec" : document.getElementById('row-' + rowId).style.background="#d7d5d5";

        }
        else {
            if (statusId) {
                if (statusId == 'Реком.' || statusId == 'Черновик') {
                    if (a_m_v < 0) {
                        document.getElementById('card_selected_for_approval_value').style.color="red";
                        document.getElementById('card_available_money_value').style.color="red";
                        document.getElementById('row-' + rowId).style.background="red";
                    }
                    else {
                        if (paymentFullStatus) {
                            document.getElementById('row-' + rowId).style.background="#61e283";
                            document.getElementById('row-' + rowId).style.borderBottom="1px solid #00000036";
                        }
                        else if (!paymentFullStatus){
                            document.getElementById('row-' + rowId).style.background="#34a853";
                            document.getElementById('row-' + rowId).style.borderBottom="solid 1px #00000036";
                        }
                    }
                }
                else {
                    document.getElementById('row-' + rowId).style.background="grey";
                }
            }
            else {
                if (a_m_v < 0) {
                    document.getElementById('card_selected_for_approval_value').style.color="red";
                    document.getElementById('card_available_money_value').style.color="red";
                    document.getElementById('row-' + rowId).style.background="red";
                }
                else {
                    if (paymentFullStatus) {
                        document.getElementById('row-' + rowId).style.background="#61e283";
                        document.getElementById('row-' + rowId).style.borderBottom="1px solid #00000036";
                    }
                    else if (!paymentFullStatus){
                        document.getElementById('row-' + rowId).style.background="#34a853";
                        document.getElementById('row-' + rowId).style.borderBottom="1px solid #00000036";
                    }
                }
            }
        }
        if (statusId && statusId === 'Черновик') {
            document.getElementById('status-' + rowId).style.background="yellow"
        }
    }

    else {
        var selectedRows = document.getElementsByName('selectedRows');
        var statusId = document.getElementsByName('status_id');

        if (statusId.length) {
            for (var i=0; i<selectedRows.length; i++) {
                if (statusId[i].value == 'Черновик') {
                    document.getElementById('status-' + (i+1)).style.background="yellow"
                }
            }
        }
    }
}
