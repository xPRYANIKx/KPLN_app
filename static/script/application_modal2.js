function getModal2(paymentId=null) {
    fetch('/update_payment/' + paymentId)
        .then(response => response.json())
        .then(data => {
            console.log(data.payment)
            console.log(data.payment[5])
            console.log(data.payment.basis_of_payment)
            console.log(data.payment['basis_of_payment'])
            console.log(typeof data.payment)
            console.log(data.payment['payment_description'])


            document.getElementById('basis_of_payment').textContent = data.payment['basis_of_payment'];

            const select = document.getElementById('responsible');
            for (let i = 0; i < select.length; i++) {
                if (select[i].value === data.payment['user_id'] + '-@@@-' + data.payment['last_name'] + ' ' + data.payment['first_name']) select[i].selected = true;
            }

            const select2 = document.getElementById('cost_items');
            for (let i = 0; i < select2.length; i++) {
                if (select2[i].value === data.payment['cost_item_id'].toString()) select2[i].selected = true;
            }

            const select3 = document.getElementById('objects_name');
            for (let i = 0; i < select3.length; i++) {
                if (select3[i].value === data.payment['object_id'].toString()) select3[i].selected = true;
            }

            document.getElementById('payment_description').textContent = data.payment['payment_description'];

            document.getElementById('partners').value = data.payment['partner'];

            document.getElementById('payment_due_date').value = data.payment['payment_due_date'];

            const select4 = document.getElementById('our_company');
            for (let i = 0; i < select3.length; i++) {
                if (select4[i].value === data.payment['contractor_id'].toString()) select4[i].selected = true;
            }

            document.getElementById('main_sum').value = data.payment['payment_sum_rub'];

            document.getElementById('sum_remain').value = data.payment['approval_sum_rub'];

            document.getElementById('payment_sum').value = data.payment['amount_rub'];

        })
        .catch(error => {
          console.error('Error:', error);
    });
};