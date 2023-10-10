
const element = document.querySelector(".showModalId");
const crossButton = document.querySelector("#crossBtn");
const closeButton = document.querySelector("#closeBtn");
const dialog = document.querySelector("#payment-approval__dialog");
const annulButton = document.querySelector("#annul__edit_btn");
//const saveButton = document.querySelector("#submitBtn");
const saveButton = document.querySelector("#save__edit_btn");


var elements = document.getElementsByClassName("showModalId");
for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener("click", function () {
        var dialog = document.getElementById("payment-approval__dialog");
        var bodyRef = document.getElementById('paid_history-table').getElementsByTagName('tbody')[0];
        bodyRef.innerHTML = ''
        dialog.showModal();
    });
}

crossButton.addEventListener("click", closeDialog);
function closeDialog() {
    dialog.close();
}
closeButton.addEventListener("click", closeDialog);
function closeDialog() {
    dialog.close();
}

annulButton.addEventListener("click", annulPayment);
function annulPayment() {
    var paymentId = document.getElementById('payment_id').textContent;
    console.log(paymentId);
    fetch('/annul_payment', {
        "headers" : {
            'Content-Type' : 'application/json'
        },
        "method": "POST",
        "body": JSON.stringify( {
            'paymentId' : paymentId
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('data', data)
        if (data.status === 'success') {
            window.location.href = '/payment-approval';
        } else {
            window.location.href = '/payment-approval';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

saveButton.addEventListener("click", savePayment);
function savePayment() {
    var paymentId = document.getElementById('payment_id').textContent;
    var basis_of_payment = document.getElementById('basis_of_payment').value;
    var responsible = document.getElementById('responsible').value;
    var cost_items = document.getElementById('cost_items').value;
    var cost_items_category = cost_items.split('-@@@-')[0];
    var cost_items_id = cost_items.split('-@@@-')[1];
    var objects_name = document.getElementById('objects_name').value;
    var payment_description = document.getElementById('payment_description').value;
    var partners = document.getElementById('partners').value;
    var payment_due_date = document.getElementById('payment_due_date').value;
    var our_company = document.getElementById('our_company').value;
    var main_sum = document.getElementById('main_sum').value;
    var payment_sum = document.getElementById('payment_sum').value;
    var payment_full_agreed_status = document.getElementById('paymentFullStatus').checked;

//    Если вид работ не субподрядчики, то удаляем id проекта
    cost_items_category !== 'Субподрядчики'? objects_name = '': 1;
console.log(cost_items_category)
console.log(
`   paymentId ${paymentId}
   basis_of_payment  ${basis_of_payment}
   responsible  ${responsible}
   cost_items  ${cost_items_id}
   objects_name  ${objects_name}
   payment_description  ${payment_description}
   partners  ${partners}
   payment_due_date  ${payment_due_date}
   our_company  ${our_company}
   main_sum  ${main_sum}
   payment_sum  ${payment_sum}
   payment_full_agreed_status  ${payment_full_agreed_status}`)




    console.log(paymentId);
    fetch('/save_payment', {
        "headers" : {
            'Content-Type' : 'application/json'
        },
        "method": "POST",
        "body": JSON.stringify( {
            'paymentId': paymentId,
            'basis_of_payment': basis_of_payment,
            'responsible': responsible,
            'cost_items': cost_items_id,
            'objects_name': objects_name,
            'payment_description': payment_description,
            'partners': partners,
            'payment_due_date': payment_due_date,
            'our_company': our_company,
            'main_sum': main_sum,
            'payment_sum': payment_sum,
            'objects_name': objects_name,
            'payment_full_agreed_status': payment_full_agreed_status,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('data', data)
        if (data.status === 'success') {
            window.location.href = '/payment-approval';
        } else {
            window.location.href = '/payment-approval';
            console.log('   else');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}