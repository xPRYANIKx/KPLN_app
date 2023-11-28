function paymentSelectAll() {
    var status = document.getElementById('selectAll').checked;
    var allRows = document.querySelectorAll('[id*="selectedRows-"]');
    var allRows_clone = Array.prototype.slice.call(allRows)
    for (i of allRows) {
        if (i.checked !== status) {
            i.checked = status;
            paymentApprovalRecalcCards(allRows_clone.indexOf(i)+1)
        }
    }
}
