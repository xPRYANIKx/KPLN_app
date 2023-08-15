function checkFormCashInflow() {
    var field1 = document.getElementById('our_company').value;
    var field2 = document.getElementById('inflow_type').value;
    var field3 = document.getElementById('cash_inflow_sum').value;
    var field4 = document.getElementById('cash_inflow_description').value;

    if (field1 !== '' && field2 !== '' && field3 !== '' && field4 !== '') {
        document.getElementById('submitBtn').disabled = false;
    } else {
        document.getElementById('submitBtn').disabled = true;
    }
}