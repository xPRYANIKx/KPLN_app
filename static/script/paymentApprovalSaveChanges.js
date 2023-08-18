function saveData(rowId) {
    var paymentNumber = document.getElementById('paymentNumber-' + rowId).value;
    var amount = document.getElementById('amount-' + rowId).value;
    var statusId = document.getElementById('status_id-' + rowId).value;
    var paymentFullAgreedStatus = document.getElementById('paymentFullAgreedStatus-' + rowId).checked;
    // Send a POST request to the server
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_quick_changes_approved_payments', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.send('row_id=' + rowId + '&payment_number=' + paymentNumber +
             '&amount=' + amount + '&status_id=' + statusId +
             '&payment_full_agreed_status=' + paymentFullAgreedStatus);
}