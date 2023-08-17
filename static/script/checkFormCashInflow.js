function checkFormCashInflow() {
    var field1 = document.getElementById('our_company').value;
    var field2 = document.getElementById('inflow_type').value.split('-@@@-')[0];
    var field3 = document.getElementById('cash_inflow_sum').value;
    var field4 = document.getElementById('cash_inflow_description').value;
    var field5 = document.getElementById('taker_company').value;

    //Внутренний платёж
    if (field2 == 4) {
        document.getElementById("taker_company_div").style.display = "flex";
        document.getElementById("taker_company").required = true;
        document.getElementById("cash_inflow_description_div").style.display = "none";
        document.getElementById("cash_inflow_description").required = false;
        $("#our_company_label").text("Откуда переводим")
    }
    else if (!field5) {
        field5 = "пусто"
    }
    if (field2 != 4) {
        document.getElementById("taker_company_div").style.display = "none";
        document.getElementById("taker_company").required = false;
        document.getElementById("cash_inflow_description_div").style.display = "flex";
        document.getElementById("cash_inflow_description").required = true;
        $("#our_company_label").text("Компания")
    }
    else if (!field4) {
        field4 = "пусто"
    }

    if (field1 !== '' && field2 !== '' && field3 !== '' && field4 !== '' && field5 !== '') {
        document.getElementById('submitBtn').disabled = false;
    } else {
        document.getElementById('submitBtn').disabled = true;
    }
}