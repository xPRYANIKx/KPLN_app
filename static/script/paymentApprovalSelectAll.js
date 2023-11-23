function paymentSelectAll() {
    var status = document.getElementById('selectAll').checked;
    console.log(status)
    var zzz = document.querySelectorAll('[id*="selectedRows-"]');
    var rrr = Array.prototype.slice.call(zzz)
    for (i of zzz) {
        i.checked = status
    }
    for (i of zzz) {
        paymentApprovalRecalcCards(rrr.indexOf(i)+1)
    }
}
