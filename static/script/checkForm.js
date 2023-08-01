function checkForm() {
    var field1 = document.getElementById('basis_of_payment').value;
    var field2 = document.getElementById('responsible').value;
    var field3 = document.getElementById('cost_items').value;
    var field4 = document.getElementById('objects_name').value;
    var field5 = document.getElementById('payment_description').value;
    var field6 = document.getElementById('payment_due_date').value;
    var field7 = document.getElementById('our_company').value;
    var field8 = document.getElementById('payment_sum').value;
    var category = field3.split('-@@@-')[0];

    if (category === 'Субподрядчики') {
        document.getElementById('objects_name_label').hidden = false;
        document.getElementById('objects_name').hidden = false;
        document.getElementById("objects_name").required = true;
    }
    else if (category && !field4) {
        field4 = "пусто"
    }

    if (category !== 'Субподрядчики') {
        document.getElementById('objects_name_label').hidden = true;
        document.getElementById('objects_name').hidden = true;
        document.getElementById("objects_name").required = false;
    }

    if (field1 !== '' && field2 !== '' && field3 !== '' && field4 !== '' && field5 !== '' && field6 !== '' &&
        field7 !== '' && field8 !== '') {
        document.getElementById('submitBtn').disabled = false;
        console.log(document.getElementById('responsible_name').value)
    } else {
        document.getElementById('submitBtn').disabled = true;
    }
}