
const element = document.querySelector(".showModalId");
const crossButton = document.querySelector("#crossBtn");
const closeButton = document.querySelector("#closeBtn");
const dialog = document.querySelector("#payment-approval__dialog");
const annulButton = document.querySelector("#annul__edit_btn");
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
    paymentId = document.getElementById('payment_id').textContent;
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
