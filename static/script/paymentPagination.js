$(document).ready(function() {

    const tableR = document.querySelector('.tableR');
    var dialog = document.getElementById("payment-approval__dialog");
    var limit = 25
    var tableR2 = document.getElementById('payment-table');

    if(tableR) {
        if ($(this).innerHeight() > tableR2.offsetHeight) {
            var sortCol_1 = document.getElementById('sortCol-1').textContent
            // document.getElementById('sortCol-1').textContent = ''
            var page_url = document.URL.substring(document.URL.lastIndexOf('/')+1);
            if (page_url === 'payment-approval') {
                paymentApproval(sortCol_1);
            }
            else if (page_url === 'payment-pay') {
                paymentPay(sortCol_1);
            }
            else if (page_url === 'payment-list') {
                paymentList(sortCol_1);
            }
            else if (page_url === 'payment-approval-list') {
                paymentList(sortCol_1);
            }
            else if (page_url === 'payment-paid-list') {
                paymentList(sortCol_1);
            }
        }
    }

    tableR.addEventListener('scroll', function() {

        var sortCol_1 = document.getElementById('sortCol-1').textContent
        if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight && sortCol_1) {
            document.getElementById('sortCol-1').textContent = ''
            var page_url = document.URL.substring(document.URL.lastIndexOf('/')+1);
            if (page_url === 'payment-approval') {
                paymentApproval(sortCol_1);
            }
            else if (page_url === 'payment-pay') {
                paymentPay(sortCol_1);
            }
            else if (page_url === 'payment-list') {
                paymentList(sortCol_1);
            }
            else if (page_url === 'payment-approval-list') {
                paymentList(sortCol_1);
            }
            else if (page_url === 'payment-paid-list') {
                paymentList(sortCol_1);
            }
            if(tableR) {
              const rect = tableR.getBoundingClientRect();
            }

            return
        }
    });

    function paymentApproval(sortCol_1) {
//        var limit = 2; // Number of contracts to load per request

        var sortCol_1_val = document.getElementById('sortCol-1_val').textContent
        var sortCol_2 = document.getElementById('sortCol-2').textContent
        var sortCol_2_val = document.getElementById('sortCol-2_val').textContent
        var sortCol_id = document.getElementById('sortCol-id').textContent
        var sortCol_id_val = document.getElementById('sortCol-id_val').textContent

        // Получили пустые данные - загрузили всю таблицу - ничего не делаем
        if (!sortCol_1) {
            return
        }
        else {

            fetch('/get-paymentApproval-pagination', {
                "headers": {
                    'Content-Type': 'application/json'
                },
                "method": "POST",
                "body": JSON.stringify({
                    'limit': limit,
                    'sort_col_1': sortCol_1,
                    'sort_col_1_val': sortCol_1_val,
                    'sort_col_2': sortCol_2,
                    'sort_col_2_val': sortCol_2_val,
                    'sort_col_id': sortCol_2,
                    'sort_col_id_val': sortCol_2_val,
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        if (!data.payment) {return}
                        document.getElementById('sortCol-1').textContent = data.sort_col['col_1'][0]
                        document.getElementById('sortCol-1_val').textContent = data.sort_col['col_1'][1]
                        document.getElementById('sortCol-2').textContent = data.sort_col['col_2'][0]
                        document.getElementById('sortCol-2_val').textContent = data.sort_col['col_2'][1]
                        document.getElementById('sortCol-id').textContent = data.sort_col['col_id'][0]
                        document.getElementById('sortCol-id_val').textContent = data.sort_col['col_id'][1]

                        const tab = document.getElementById("payment-table");
                        var tab_tr = tab.getElementsByTagName('tbody')[0];
                        var tab_numRow = tab.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
                        var numRow = parseInt(tab_numRow[tab_numRow.length-1].getElementsByTagName('td')[0].getElementsByTagName('input')[0].value)

                        var tab_tr0 = tab.getElementsByTagName('tbody')[0]

                        for (pmt of data.payment) {

                            numRow++;
                            // Вставляем ниже новую ячейку, копируя предыдущую
                            var table2 = document.getElementById("payment-table");
                            var rowCount = table2.rows.length;
                            var lastRow = table2.rows[rowCount - 1];
                            var newRow = lastRow.cloneNode(true);

                            var td = newRow.getElementsByTagName('td'); // Ячейки новой строки

                            //////////////////////////////////////////
                            // Меняем данные в ячейке
                            //////////////////////////////////////////
                            // id
                            newRow.id = `row-${numRow}`;

                            // Флажок выбора
                            td_0 = td[0];
                            td_0_input = td_0.getElementsByTagName('input')[0];
                            td_0.dataset.sort = '0';
                            td_0_input.id = `selectedRows-${numRow}`;
                            td_0_input.value  = numRow;
                            td_0_input.setAttribute("onchange", `paymentApprovalRecalcCards(${numRow}), paymentApprovalNoSelect(${numRow}), refreshSortValChb(${numRow})`);
                            td_0_input.checked = false;

                            // Описание
                            td_1 = td[1];
                            td_1.dataset.sort = `${pmt['descr_part1']}: ${pmt['payment_description']}`;
                            td_1.setAttribute("title", `${pmt['descr_part1']}\n${pmt['payment_description']}`);
                            td_1.setAttribute("onclick", `getModal(${pmt['payment_id']})`);
                            td_1.textContent = ''
                            var td_1_span = document.createElement("span");
                            td_1_span.classList.add("paymentFormBold");
                            td_1_span.textContent = `${pmt['descr_part1']}:`;
                            var td_1_textContent = document.createTextNode(pmt['payment_description_short']);
                            td_1.appendChild(td_1_span);
                            td_1.appendChild(document.createElement("BR"));
                            td_1.appendChild(td_1_textContent);

                            // Общая сумма
                            td_2 = td[2];
                            td_2.dataset.sort = pmt['payment_sum'];
                            td_2.textContent = pmt['payment_sum_rub'];

                            // Остаток к оплате
                            td_3 = td[3];
                            td_3.dataset.sort = pmt['approval_sum'];
                            var td_3_input = document.createElement("input");
                            td_3_input.type = "text";
                            td_3_input.id = `approvalSum-${numRow}`;
                            td_3_input.name = "approval_sum";
                            td_3_input.value = pmt['approval_sum'];
                            td_3_input.setAttribute('hidden', 'hidden');
                            td_3_input.setAttribute('readonly', true);
                            td_3.textContent = pmt['approval_sum_rub'];
                            td_3.appendChild(td_3_input);

                            // Согласованная сумма
                            td_4 = td[4];
                            td_4.dataset.sort = pmt['amount'];
                            td_4.textContent = ''
                            var td_4_input = document.createElement("input");
                            td_4_input.type = "text";
                            td_4_input.id = `amount-${numRow}`;
                            td_4_input.name = "amount";
                            td_4_input.value = pmt['amount_rub'];
                            td_4_input.dataset.amount = 0;
                            td_4_input.setAttribute("onchange", `paymentApprovalRecalcCards(${numRow}), saveData(${numRow}, '${data.page}'), refreshSortValAmount(${numRow})`)
                            td_4.appendChild(td_4_input);

                            // Ответственный
                            td_5 = td[5];
                            td_5.dataset.sort = `${pmt['last_name']} ${pmt['first_name']}`;
                            td_5.textContent = `${pmt['last_name']} ${pmt['first_name'][0]}.`;

                            // Срок оплаты
                            td_6 = td[6];
                            td_6.dataset.sort = pmt['payment_due_date'];
                            td_6.textContent = pmt['payment_due_date_txt'];

                            // Статус
                            td_7 = td[7];
                            td_7.id = `status-${numRow}`;
                            td_7.dataset.sort = pmt['status_id'];
                            td_7_select = td_7.getElementsByTagName('select')[0];
                            td_7_select.id = `status_id-${numRow}`;
                            td_7_select.setAttribute("onchange", `paymentApprovalRecalcCards(${numRow}), saveData(${numRow}, '${data.page}')`)

//                            for (let i = 0; i < td_7_select.length; i++) {
//                                if (td_7_select[i].value === pmt['status_name'].toString()) td_7_select[i].selected = true;
//                            }

                            // Дата создания
                            td_8 = td[8];
                            td_8.dataset.sort = pmt['payment_at'];
                            var td_8_input = document.createElement("input");
                            td_8_input.type = "text";
                            td_8_input.id = `paymentNumber-${numRow}`;
                            td_8_input.name = "payment_number";
                            td_8_input.value = pmt['payment_id'];
                            td_8_input.setAttribute('hidden', 'hidden');
                            td_8_input.setAttribute('readonly', true);
                            td_8.textContent = pmt['payment_at_txt'];
                            td_8.appendChild(td_8_input);

                            // До полной оплаты
                            td_9 = td[9];
                            td_9_input = td_9.getElementsByTagName('input')[0];
                            pmt['payment_full_agreed_status']? td_9.dataset.sort=1: td_9.dataset.sort = 0;
                            td_9_input.id = `paymentFullStatus-${numRow}`;
                            td_9_input.value  = numRow;
                            td_9_input.setAttribute("onchange", `saveData(${numRow}, '${data.page}'), tabColorize(${numRow}), refreshSortValChb(${numRow})`);
                            td_9_input.checked = pmt['payment_full_agreed_status'];

                            tab_tr0.appendChild(newRow);

                            const scrollPercentage = ((rowCount) / data.tab_rows) * 100;
                            const progressBar = document.querySelector('.progress');
                            progressBar.style.width = scrollPercentage + '%';

                            tabColorize(numRow);
                        }
                        return
                    }
                    else if (data.status === 'error') {
                        alert(data.description)
                    }
                    else {
                        window.location.href = '/payment-approval';
                    }
            })
            .catch(error => {
            console.error('Error:', error);
        });
        }
    };

    function paymentPay(sortCol_1) {
//        var limit = 2; // Number of contracts to load per request

        var sortCol_1_val = document.getElementById('sortCol-1_val').textContent
        var sortCol_2 = document.getElementById('sortCol-2').textContent
        var sortCol_2_val = document.getElementById('sortCol-2_val').textContent
        var sortCol_id = document.getElementById('sortCol-id').textContent
        var sortCol_id_val = document.getElementById('sortCol-id_val').textContent

        // Получили пустые данные - загрузили всю таблицу - ничего не делаем
        if (!sortCol_1) {
            return
        }
        else {

            fetch('/get-paymentPay-pagination', {
                "headers": {
                    'Content-Type': 'application/json'
                },
                "method": "POST",
                "body": JSON.stringify({
                    'limit': limit,
                    'sort_col_1': sortCol_1,
                    'sort_col_1_val': sortCol_1_val,
                    'sort_col_2': sortCol_2,
                    'sort_col_2_val': sortCol_2_val,
                    'sort_col_id': sortCol_2,
                    'sort_col_id_val': sortCol_2_val,
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        if (!data.payment) {return}
                        document.getElementById('sortCol-1').textContent = data.sort_col['col_1'][0]
                        document.getElementById('sortCol-1_val').textContent = data.sort_col['col_1'][1]
                        document.getElementById('sortCol-2').textContent = data.sort_col['col_2'][0]
                        document.getElementById('sortCol-2_val').textContent = data.sort_col['col_2'][1]
                        document.getElementById('sortCol-id').textContent = data.sort_col['col_id'][0]
                        document.getElementById('sortCol-id_val').textContent = data.sort_col['col_id'][1]

                        const tab = document.getElementById("payment-table");
                        var tab_tr = tab.getElementsByTagName('tbody')[0];
                        var tab_numRow = tab.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
                        var numRow = parseInt(tab_numRow[tab_numRow.length-1].getElementsByTagName('td')[0].getElementsByTagName('input')[0].value)

                        var tab_tr0 = tab.getElementsByTagName('tbody')[0]

                        for (pmt of data.payment) {

                            numRow++;
                            // Вставляем ниже новую ячейку, копируя предыдущую
                            var table2 = document.getElementById("payment-table");
                            var rowCount = table2.rows.length;
                            var lastRow = table2.rows[rowCount - 1];
                            var newRow = lastRow.cloneNode(true);

                            var td = newRow.getElementsByTagName('td'); // Ячейки новой строки

                            //////////////////////////////////////////
                            // Меняем данные в ячейке
                            //////////////////////////////////////////
                            // id
                            newRow.id = `row-${numRow}`;

                            // Флажок выбора
                            td_0 = td[0];
                            td_0_input = td_0.getElementsByTagName('input')[0];
                            td_0.dataset.sort = '0';
                            td_0_input.id = `selectedRows-${numRow}`;
                            td_0_input.value  = numRow;
                            td_0_input.setAttribute("onchange", `paymentApprovalRecalcCards(${numRow}), paymentApprovalNoSelect(${numRow}), refreshSortValChb(${numRow})`);
                            td_0_input.checked = false;

                            // Статья затрат
                            td_1 = td[1];
                            td_1.id = `category-${numRow}`;
                            td_1.dataset.sort = pmt['cost_item_name'];
                            td_1.setAttribute("onclick", `getModal(${pmt['payment_id']})`);
                            var td_1_input = document.createElement("input");
                            td_1_input.type = "text";
                            td_1_input.id = `paymentNumber-${numRow}`;
                            td_1_input.name = "payment_number";
                            td_1_input.value = pmt['payment_id'];
                            td_1_input.setAttribute('hidden', 'hidden');
                            td_1_input.setAttribute('readonly', true);
                            td_1.textContent = pmt['cost_item_name'];
                            td_1.appendChild(td_1_input);

                            // Номер платежа
                            td_2 = td[2];
                            td_2.dataset.sort = pmt['payment_id'];
                            td_2.textContent = pmt['payment_number'];
                            td_2.setAttribute("onclick", `getModal(${pmt['payment_id']})`);

                            // Наименование платежей
                            td_3 = td[3];
                            td_3.dataset.sort = pmt['basis_of_payment'];
                            td_3.setAttribute("title", pmt['basis_of_payment']);
                            td_3.setAttribute("onclick", `getModal(${pmt['payment_id']})`);
                            td_3.textContent = pmt['basis_of_payment'];
                            td_3.addEventListener("click", function () {
                                var bodyRef = document.getElementById('paid_history-table').getElementsByTagName('tbody')[0];
                                bodyRef.innerHTML = ''
                                var logDPage = document.getElementById('logDPage__content__text');
                                logDPage.innerHTML = ''
                                dialog.showModal();
                            });

                            // Описание
                            td_4 = td[4];
                            td_4.dataset.sort = `${pmt['basis_of_payment']}: ${pmt['payment_description']}`;
                            td_4.setAttribute("title", pmt['payment_description']);
                            td_4.setAttribute("onclick", `getModal(${pmt['payment_id']})`);
                            td_4.textContent = '';
                            var td_4_input = document.createElement("input");
                            td_4_input.name = "contractor_id";
                            td_4_input.value = pmt['contractor_id'];
                            td_4_input.setAttribute('hidden', 'hidden');
                            td_4_input.setAttribute('readonly', true);
                            var td_4_span = document.createElement("span");
                            td_4_span.classList.add("paymentFormBold");
                            td_4_span.textContent = `${pmt['contractor_name']}: `;
                            var td_4_textContent = document.createTextNode(pmt['payment_description']);
                            td_4.appendChild(td_4_input);
                            td_4.appendChild(td_4_span);
                            td_4.appendChild(td_4_textContent);

                            // Объект
                            td_5 = td[5];
                            td_5.dataset.sort = pmt['object_name'];
                            td_5.textContent = pmt['object_name'];
                            td_5.setAttribute("onclick", `getModal(${pmt['payment_id']})`);

                            // Ответственный
                            td_6 = td[6];
                            td_6.dataset.sort = `${pmt['last_name']} ${pmt['first_name']}`;
                            td_6.textContent = `${pmt['last_name']} ${pmt['first_name'][0]}.`;
                            td_6.setAttribute("onclick", `getModal(${pmt['payment_id']})`);

                            // Контрагент
                            td_7 = td[7];
                            td_7.dataset.sort = pmt['partner'];
                            td_7.textContent = pmt['partner'];
                            td_7.setAttribute("onclick", `getModal(${pmt['payment_id']})`);

                            // Общая сумма
                            td_8 = td[8];
                            td_8.dataset.sort = pmt['payment_sum'];
                            td_8.textContent = pmt['payment_sum_rub'];
                            td_8.setAttribute("onclick", `getModal(${pmt['payment_id']})`);

                            // Оплачено
                            td_9 = td[9];
                            td_9.dataset.sort = pmt['paid_sum'];
                            td_9.textContent = pmt['paid_sum_rub'];
                            td_9.setAttribute("onclick", `getModal(${pmt['payment_id']})`);

                            // Согласованная сумма
                            td_10 = td[10];
                            td_10.dataset.sort = pmt['approval_sum'];
                            td_10.setAttribute("onclick", `getModal(${pmt['payment_id']})`);
                            var td_10_input = document.createElement("input");
                            td_10_input.type = "text";
                            td_10_input.id = `approvalSum-${numRow}`;
                            td_10_input.name = "approval_sum";
                            td_10_input.value = pmt['approval_sum'];
                            td_10_input.setAttribute('hidden', 'hidden');
                            td_10_input.setAttribute('readonly', true);
                            td_10.textContent = pmt['approval_sum_rub'];
                            td_10.appendChild(td_10_input);

                            // Сумма к оплате
                            td_11 = td[11];
                            td_11.dataset.sort = pmt['amount'];
                            td_11.textContent = ''
                            var td_11_input = document.createElement("input");
                            td_11_input.type = "text";
                            td_11_input.id = `amount-${numRow}`;
                            td_11_input.name = "amount";
                            td_11_input.value = pmt['amount_rub'];
                            td_11_input.dataset.amount = 0;
                            td_11_input.setAttribute("onchange", `paymentApprovalRecalcCards(${numRow}), saveData(${numRow}, '${data.page}'), refreshSortValChb(${numRow})`)
                            td_11.appendChild(td_11_input);

                            // Срок оплаты
                            td_12 = td[12];
                            td_12.dataset.sort = pmt['payment_due_date'];
                            td_12.textContent = pmt['payment_due_date_txt'];
                            td_12.setAttribute("onclick", `getModal(${pmt['payment_id']})`);

                            // Дата создания
                            td_13 = td[13];
                            td_13.dataset.sort = pmt['payment_at'];
                            td_13.textContent = pmt['payment_at_txt'];
                            td_13.setAttribute("onclick", `getModal(${pmt['payment_id']})`);

                            // До полной оплаты
                            td_14 = td[14];
                            td_14_input = td_14.getElementsByTagName('input')[0];
                            pmt['payment_full_agreed_status']? td_14.dataset.sort=1:td_14.dataset.sort='0';
                            td_14_input.id = `paymentFullStatus-${numRow}`;
                            td_14_input.value  = numRow;
                            td_14_input.setAttribute("onchange", `saveData(${numRow}, '${data.page}'), tabColorize(${numRow}), refreshSortValChb(${numRow})`);
                            td_14_input.checked = pmt['payment_full_agreed_status'];

                            tab_tr0.appendChild(newRow);

                            const scrollPercentage = ((rowCount) / data.tab_rows) * 100;
                            const progressBar = document.querySelector('.progress');
                            progressBar.style.width = scrollPercentage + '%';

                            tabColorize(numRow);
                        }
                        return
                    }
                    else if (data.status === 'error') {
                        alert(data.description)
                    }
                    else {
                        window.location.href = '/payment-pay';
                    }
            })
            .catch(error => {
            console.error('Error:', error);
        });
        }
    }

    function paymentList(sortCol_1) {
//        var limit = 2; // Number of contracts to load per request

        var sortCol_1_val = document.getElementById('sortCol-1_val').textContent
        var sortCol_2 = document.getElementById('sortCol-2').textContent
        var sortCol_2_val = document.getElementById('sortCol-2_val').textContent
        var sortCol_id = document.getElementById('sortCol-id').textContent
        var sortCol_id_val = document.getElementById('sortCol-id_val').textContent
        var fetchFunc = ''; // Название вызываемой функции в fetch
        var col_shift = 0; // Сдвиг колонок
        var col_shift2 = 0; // Сдвиг колонок
        var page_url = document.URL.substring(document.URL.lastIndexOf('/')+1);

        if (page_url == 'payment-list') {
            fetchFunc = '/get-paymentList-pagination';
        }
        else if (page_url == 'payment-approval-list') {
            fetchFunc = '/get-paymentApprovalList-pagination';
            col_shift = 1;
        }
        else if (page_url == 'payment-paid-list') {
            fetchFunc = '/get-paymentPaidList-pagination';
            col_shift = 1;
            col_shift2 = 1;
        }

        // Получили пустые данные - загрузили всю таблицу - ничего не делаем
        if (!sortCol_1) {
            return
        }
        else {

            fetch(fetchFunc, {
                "headers": {
                    'Content-Type': 'application/json'
                },
                "method": "POST",
                "body": JSON.stringify({
                    'limit': limit,
                    'sort_col_1': sortCol_1,
                    'sort_col_1_val': sortCol_1_val,
                    'sort_col_2': sortCol_2,
                    'sort_col_2_val': sortCol_2_val,
                    'sort_col_id': sortCol_2,
                    'sort_col_id_val': sortCol_2_val,
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        if (!data.payment) {return}
                        document.getElementById('sortCol-1').textContent = data.sort_col['col_1'][0]
                        document.getElementById('sortCol-1_val').textContent = data.sort_col['col_1'][1]
                        document.getElementById('sortCol-2').textContent = data.sort_col['col_2'][0]
                        document.getElementById('sortCol-2_val').textContent = data.sort_col['col_2'][1]
                        document.getElementById('sortCol-id').textContent = data.sort_col['col_id'][0]
                        document.getElementById('sortCol-id_val').textContent = data.sort_col['col_id'][1]

                        const tab = document.getElementById("payment-table");
                        var tab_tr = tab.getElementsByTagName('tbody')[0];
                        var tab_numRow = tab.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
                        var numRow = parseInt(tab_numRow[tab_numRow.length-1].dataset.sort)

                        var tab_tr0 = tab.getElementsByTagName('tbody')[0]

                        for (pmt of data.payment) {

                            numRow++;
                            // Вставляем ниже новую ячейку, копируя предыдущую
                            var table2 = document.getElementById("payment-table");
                            var rowCount = table2.rows.length;
                            var lastRow = table2.rows[rowCount - 1];
                            var newRow = lastRow.cloneNode(true);

                            var td = newRow.getElementsByTagName('td'); // Ячейки новой строки

                            //////////////////////////////////////////
                            // Меняем данные в ячейке
                            //////////////////////////////////////////
                            // id
                            newRow.id = `row-${numRow}`;
                            newRow.dataset.sort = numRow;

                            if (page_url == 'payment-approval-list') {
                                newRow.setAttribute("onclick", `getModal(${pmt['payment_id']})`);

                                newRow.addEventListener("click", function () {
                                    var bodyRef = document.getElementById('paid_history-table').getElementsByTagName('tbody')[0];
                                    bodyRef.innerHTML = ''
                                    var logDPage = document.getElementById('logDPage__content__text');
                                    logDPage.innerHTML = ''
                                    dialog.showModal();
                                });

                            }
                            
                            if (page_url == 'payment-paid-list') {
                                // Согласованная сумма
                                td_column_shift1 = td[0];
                                td_column_shift1.dataset.sort = numRow;
                                td_column_shift1.textContent = numRow;
                            }

                            // Номер платежа
                            td_0 = td[0+col_shift2];
                            td_0.dataset.sort = pmt['payment_id'];
                            td_0.textContent = pmt['payment_number'];

                            // Статья затрат
                            td_1 = td[1+col_shift2];
                            td_1.dataset.sort = pmt['cost_item_name'];
                            td_1.textContent = pmt['cost_item_name'];

                            // Номер платежа
                            td_2 = td[2+col_shift2];
                            td_2.dataset.sort = pmt['basis_of_payment'];
                            td_2.setAttribute("title", pmt['basis_of_payment']);
                            td_2.textContent = pmt['basis_of_payment_short'];

                            // Описание
                            td_3 = td[3+col_shift2];
                            td_3.dataset.sort = `${pmt['basis_of_payment']}: ${pmt['payment_description']}`;
                            td_3.setAttribute("title", pmt['payment_description']);
                            td_3.textContent = '';
                            var td_3_span = document.createElement("span");
                            td_3_span.classList.add("paymentFormBold");
                            td_3_span.textContent = `${pmt['contractor_name']}: `;
                            var td_3_textContent = document.createTextNode(pmt['payment_description_short']);
                            td_3.appendChild(td_3_span);
                            td_3.appendChild(td_3_textContent);

                            // Объект
                            td_4 = td[4+col_shift2];
                            td_4.dataset.sort = pmt['object_name'];
                            td_4.textContent = pmt['object_name'];

                            // Ответственный
                            td_5 = td[5+col_shift2];
                            td_5.dataset.sort = `${pmt['last_name']} ${pmt['first_name']}`;
                            td_5.textContent = `${pmt['last_name']} ${pmt['first_name'][0]}.`;

                            // Контрагент
                            td_6 = td[6+col_shift2];
                            td_6.dataset.sort = pmt['partner'];
                            td_6.textContent = pmt['partner'];

                            // Общая сумма
                            td_7 = td[7+col_shift2];
                            td_7.dataset.sort = pmt['payment_sum'];
                            td_7.textContent = pmt['payment_sum_rub'];

                            if (page_url == 'payment-approval-list' || page_url == 'payment-paid-list') {
                                // Согласованная сумма
                                td_column_shift1 = td[7+col_shift+col_shift2];
                                td_column_shift1.dataset.sort = pmt['approval_sum'];
                                td_column_shift1.textContent = pmt['approval_sum_rub'];
                            }

                            // Оплаченная сумма
                            td_8 = td[8+col_shift+col_shift2];
                            td_8.dataset.sort = pmt['paid_sum'];
                            td_8.textContent = pmt['paid_sum_rub'];

                            // Срок оплаты
                            td_9 = td[9+col_shift+col_shift2];
                            td_9.dataset.sort = pmt['payment_due_date'];
                            td_9.textContent = pmt['payment_due_date_txt'];

                            // Дата создания
                            td_10 = td[10+col_shift+col_shift2];
                            td_10.dataset.sort = pmt['payment_at'];
                            td_10.textContent = pmt['payment_at_txt'];

                            // Дата согласования
                            if (page_url === 'payment-approval-list') {
                                td_11 = td[11+col_shift+col_shift2];
                                td_11.dataset.sort = pmt['create_at'];
                                td_11.textContent = pmt['create_at_txt'];
                            }


                            tab_tr0.appendChild(newRow);

                            const scrollPercentage = ((rowCount) / data.tab_rows) * 100;
                            const progressBar = document.querySelector('.progress');
                            progressBar.style.width = scrollPercentage + '%';
                        }
                        return
                    }
                    else if (data.status === 'error') {
                        alert(data.description)
                    }
                    else {
                        window.location.href = '/payment-approval';
                    }
            })
            .catch(error => {
            console.error('Error:', error);
        });
        }
    }

});

