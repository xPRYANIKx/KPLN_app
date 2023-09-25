function sortTable(column, type_col = 'str') {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("payment-table");
    switching = true;
    // Set the sorting direction to ascending
    dir = "asc";
    rows = table.getElementsByTagName("tr");
    while (switching) {
        switching = false;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[column];
            y = rows[i + 1].getElementsByTagName("td")[column];
            console.log(x.dataset.sort);

            // Тип данных в колонки - строка
            if (type_col == 'str') {
                if (dir == "asc") {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
                else if (dir == "desc") {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
            }
            // Тип данных в колонки - цифра
            else if (type_col == "num") {
                if (Number(x.innerHTML) && Number(y.innerHTML)) {
                    if (dir == "asc") {
                        if (Number(x.innerHTML) > Number(y.innerHTML)) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                    else if (dir == "desc") {
                        if (Number(x.innerHTML) < Number(y.innerHTML)) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
            }


        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            for (i = 1; i < (rows.length - 1); i++) {
            }
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }

    for (i = 1; i < rows.length; i++) {
        // у всех чекбоксов меняем значение value
        for (var i1 = 0; i1 < rows[i].getElementsByTagName("td").length; i1++) {
            try {
                var sub_elem = rows[i].getElementsByTagName("td")[i1].getElementsByTagName("input")[0]
                if (sub_elem.getAttribute('type') === 'checkbox') {
                    sub_elem.setAttribute("value", i);
                }
            }
            catch {
            }
        }
    }
}

function sortTable2() {
    console.log('----', new Date())
    var getCellValue = (tr, idx) => tr.children[idx].dataset['sort'];
    console.log(0)
    var comparer = (idx, asc) => (a, b) =>
        ((v1, v2) => v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : (console.log('   -   v1', v1), console.log('   -   v2', v2), v1.toString().localeCompare(v2)))
            (getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

    console.log(1)

    document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
        console.log(2)
        var table = th.closest('table');
        console.log(3)
        var tbody = table.querySelector('tbody');
        console.log(4)
        Array.from(tbody.querySelectorAll('tr'))
            .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
            .forEach(tr => tbody.appendChild(tr));
    })));

    //document.querySelectorAll('th').forEach(th => {
    //  console.log(2)
    //  var table = th.closest('table');
    //  console.log(3)
    //  var tbody = table.querySelector('tbody');
    //  console.log(4)
    //  console.log(tbody.querySelectorAll('th'))
    //  Array.from(tbody.querySelectorAll('tr'))
    //    .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
    //    .forEach(tr => tbody.appendChild(tr) );
    //});

    //document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
    //  console.log(2)
    //  var table = th.closest('table');
    //  console.log(3)
    //  var tbody = table.querySelector('tbody');
    //  console.log(4)
    //  Array.from(tbody.querySelectorAll('tr'))
    //    .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
    //    .forEach(tr => tbody.appendChild(tr) );
    //})));
}