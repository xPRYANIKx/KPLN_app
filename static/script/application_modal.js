function getModal(paymentId = null) {
    fetch('/get_card_payment/' + paymentId)
        .then(response => response.json())
        .then(data => {
            //            console.log(data)
            //            console.log(data.payment)
            //            console.log(data.paid)
            //            console.log(data.payment.basis_of_payment)
            //            console.log(data.payment['basis_of_payment'])
            //            console.log(typeof data.payment)
            //            console.log(data.payment['payment_description'])

            document.getElementById('payment_id').textContent = data.payment['payment_id'];
            document.getElementById('payment_number').textContent = data.payment['payment_number'];

            document.getElementById('basis_of_payment').textContent = data.payment['basis_of_payment'];

            const select = document.getElementById('responsible');
            for (let i = 0; i < select.length; i++) {
                if (select[i].value === data.payment['user_id'].toString()) select[i].selected = true;
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

            document.getElementById('historic_approval_sum').textContent = data.payment['historic_approval_sum_rub'];

            if (data.paid.length) {
                let history_table = document.getElementById('history_tb');
                for (let i = 0; i < data.paid.length; i++) {
                    let newRow = document.createElement("tr");

                    let newCell1 = document.createElement("td");
                    newCell1.innerHTML = data.paid[i][1];

                    let newCell2 = document.createElement("td");
//                    newCell2.innerHTML = data.paid[i][3].split(' ')[0];
                    newCell2.innerHTML = data.paid[i][3];

                    let newCell3 = document.createElement("td");
                    newCell3.innerHTML = data.paid[i][5];

                    newRow.appendChild(newCell1);
                    newRow.appendChild(newCell2);
                    newRow.appendChild(newCell3);

                    history_table.appendChild(newRow);
                }

                document.getElementById('historic_paid_sum').textContent = data.paid[0][6];
            }
            else {
                document.getElementById('historic_paid_sum').textContent = '';
            }
            document.getElementById('logs').textContent = data.logs
        })
        .catch(error => {
            console.error('Error:', error);
        });
};