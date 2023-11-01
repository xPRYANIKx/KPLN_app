function saveData(rowId, page='') {
    var paymentSelectedRows = document.getElementById('selectedRows-' + rowId).checked;
    var paymentNumber = document.getElementById('paymentNumber-' + rowId).value;
    var approvalSum = document.getElementById('approvalSum-' + rowId).value;
    var amount = document.getElementById('amount-' + rowId).value;
    var statusId = document.getElementById('status_id-' + rowId);
    var paymentFullStatus = document.getElementById('paymentFullStatus-' + rowId).checked;

//    // Для сортировки. обновляем значение
//    if (paymentSelectedRows) {
//        document.getElementById('row-' + rowId).getElementsByTagName('td')[0].dataset.sort=1;
//        console.log(1)
//    }
//    else {
//        document.getElementById('row-' + rowId).getElementsByTagName('td')[0].dataset.sort=0;
//        console.log(0)
//    }




    if (statusId) {
        statusId = document.getElementById('status_id-' + rowId).value
    }
    // Если согласованная сумма больше остатка, приравниваем согл.сум к остатку
    if (amount && parseFloat(amount) > parseFloat(approvalSum)) {
        document.getElementById('amount-' + rowId).value = approvalSum;
        amount = approvalSum;
    }
    // Send a POST request to the server
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_quick_changes_approved_payments', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
//    console.log(`'row_id=' ${rowId} \n'&payment_number=' + ${paymentNumber} \n'&amount=' + ${amount} \n'&status_id=' + ${statusId}
//'&payment_full_agreed_status=' + ${paymentFullStatus} \n'&page=' + ${page}`)

    xhr.send('row_id=' + rowId + '&payment_number=' + paymentNumber + '&amount=' + amount + '&status_id=' + statusId +
             '&payment_full_agreed_status=' + paymentFullStatus + '&page=' + page);
}
