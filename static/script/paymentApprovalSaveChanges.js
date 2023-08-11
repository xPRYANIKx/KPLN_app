function saveData(rowId) {
    var paymentNumber = document.getElementById('payment_number-' + rowId).value;
    var amount = document.getElementById('amount-' + rowId).value;
    var statusId = document.getElementById('status_id-' + rowId).value;
    var paymentFullAgreedStatus = document.getElementById('payment_full_agreed_status-' + rowId).checked;

    // Send a POST request to the server
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_quick_changes_approved_payments', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
//  Printing a success message to the console
//    xhr.onreadystatechange = function() {
//        if (xhr.readyState === 4 && xhr.status === 200) {
//            console.log('Data saved successfully');
//        }
//    };

    xhr.send('row_id=' + rowId + '&payment_number=' + paymentNumber +
             '&amount=' + amount + '&status_id=' + statusId +
             '&payment_full_agreed_status=' + paymentFullAgreedStatus);
}