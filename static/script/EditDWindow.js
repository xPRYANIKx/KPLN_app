
const element = document.querySelector(".showModalId");
const crossButton = document.querySelector("#crossBtn");
const closeButton = document.querySelector("#closeBtn");
const dialog = document.querySelector("#payment-approval__dialog");
const annulPaymentButton = document.querySelector("#annul__edit_btn");
const annulApprovalButton = document.querySelector("#annul_approval__edit_btn");
//const saveButton = document.querySelector("#submitBtn");
const saveButton = document.querySelector("#save__edit_btn");


var elements = document.getElementsByClassName("showModalId");
for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener("click", function () {
        var dialog = document.getElementById("payment-approval__dialog");
        var bodyRef = document.getElementById('paid_history-table').getElementsByTagName('tbody')[0];
        bodyRef.innerHTML = ''
        var logDPage = document.getElementById('logDPage__content__text');
        logDPage.innerHTML = ''
        dialog.showModal();
        ;
        
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

annulPaymentButton.addEventListener("click", annulPayment);
function annulPayment() {
    var paymentId = document.getElementById('payment_id').textContent;
    console.log(paymentId);
    fetch('/annul_payment', {
        "headers": {
            'Content-Type': 'application/json'
        },
        "method": "POST",
        "body": JSON.stringify({
            'paymentId': paymentId
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

annulApprovalButton.addEventListener("click", annulApproval);
function annulApproval() {
    var paymentId = document.getElementById('payment_id').textContent;
    console.log(paymentId);
    fetch('/annul_approval_payment', {
        "headers": {
            'Content-Type': 'application/json'
        },
        "method": "POST",
        "body": JSON.stringify({
            'paymentId': paymentId
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

const crossButtonInside = document.querySelector("#crossBtnInside");
const closeButtonInside = document.querySelector("#closeBtnInside");
const dialogInside = document.querySelector("#logDPage");


crossButtonInside.addEventListener("click", closeDialogInside);
function closeDialogInside() {
    dialogInside.close();
}
closeButtonInside.addEventListener("click", closeDialogInside);
function closeDialogInside() {
    dialogInside.close();
}

saveButton.addEventListener("click", savePayment);
function savePayment() {
    var paymentId = document.getElementById('payment_id').textContent;
    var basis_of_payment = document.getElementById('basis_of_payment').value;
    var basis_of_payment_dataset = document.getElementById('basis_of_payment').dataset.value;
    var responsible = document.getElementById('responsible').value;
    var responsible_dataset = document.getElementById('responsible').dataset.value;
    var cost_items = document.getElementById('cost_items').value;
    var cost_items_category = cost_items.split('-@@@-')[0];
    var cost_items_id = cost_items.split('-@@@-')[1];
    var cost_items_id_dataset = document.getElementById('cost_items').dataset.value;
    var objects_name = document.getElementById('objects_name').value;
    var objects_name_dataset = document.getElementById('objects_name').dataset.value;
    var payment_description = document.getElementById('payment_description').value;
    var payment_description_dataset = document.getElementById('payment_description').dataset.value;
    var partners = document.getElementById('partners').value;
    var partners_dataset = document.getElementById('partners').dataset.value;
    var payment_due_date = document.getElementById('payment_due_date').value;
    var payment_due_date_dataset = document.getElementById('payment_due_date').dataset.value;
    var our_company = document.getElementById('our_company').value;
    var our_company_dataset = document.getElementById('our_company').dataset.value;
    var sum_payment = document.getElementById('payment_sum').value;
    var sum_payment_dataset = document.getElementById('payment_sum').dataset.value;
    var sum_approval = document.getElementById('sum_approval').value;
    var sum_approval_dataset = document.getElementById('sum_approval').dataset.value;
    var payment_full_agreed_status = document.getElementById('paymentFullStatus').checked;
    var payment_full_agreed_status_dataset = document.getElementById('paymentFullStatus').dataset.value;

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
   sum_payment  ${sum_payment}
   sum_approval  ${sum_approval}
   payment_full_agreed_status  ${payment_full_agreed_status}`)

    fetch('/save_payment', {
        "headers" : {
            'Content-Type' : 'application/json'
        },
        "method": "POST",
        "body": JSON.stringify( {
                'payment_id': paymentId,
                'basis_of_payment': basis_of_payment,
            'basis_of_payment_dataset': basis_of_payment_dataset,
                'responsible': responsible,
            'responsible_dataset': responsible_dataset,
                'cost_item_id': cost_items_id,
            'cost_item_id_dataset': cost_items_id_dataset,
                'object_id': objects_name,
            'object_id_dataset': objects_name_dataset,
                'payment_description': payment_description,
            'payment_description_dataset': payment_description_dataset,
                'partners': partners,
            'partners_dataset': partners_dataset,
                'payment_due_date': payment_due_date,
            'payment_due_date_dataset': payment_due_date_dataset,
                'our_company_id': our_company,
            'our_company_id_dataset': our_company_dataset,
                'payment_sum': sum_payment,
            'payment_sum_dataset': sum_payment_dataset,
                'sum_approval': sum_approval,
            'sum_approval_dataset': sum_approval_dataset,
                'payment_full_agreed_status': payment_full_agreed_status,
            'p_full_agreed_s_dataset': payment_full_agreed_status_dataset
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