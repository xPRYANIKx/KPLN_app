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
            x = rows[i].getElementsByTagName("td")[column].dataset.sort;
            y = rows[i + 1].getElementsByTagName("td")[column].dataset.sort;

            // Тип данных в колонки - строка
            if (type_col == "str") {
                if (dir == "asc") {
                    if (x.toLowerCase() > y.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
                else if (dir == "desc") {
                    if (x.toLowerCase() < y.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
            }
            // Тип данных в колонки - цифра
            else if (type_col == "num") {
                if (dir == "asc") {
                    if (parseFloat(x) > parseFloat(y)) {
                        shouldSwitch = true;
                        break;
                    }
                }
                else if (dir == "desc") {
                    if (parseFloat(x) < parseFloat(y)) {
                        shouldSwitch = true;
                        break;
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

    // Список колонок с чекбоксом
    checkbox_col_num = [];
    for (var i1 = 0; i1 < rows[1].getElementsByTagName("td").length; i1++) {
        try {
            if (rows[1].getElementsByTagName("td")[i1].getElementsByTagName("input")[0].getAttribute('type') === 'checkbox') {
                checkbox_col_num.push(i1);
            }
        }
        catch {
        }
    }

    // у всех чекбоксов меняем значение value
    if (checkbox_col_num.length) {
        for (i = 1; i < rows.length; i++) {
            for (j of checkbox_col_num) {
                rows[i].getElementsByTagName("td")[j].getElementsByTagName("input")[0].setAttribute("value", i);
            }
        }
    }

    // Стрелки в шапке таблицы
    var col_cnt = rows[0].getElementsByTagName("th").length
    console.log(col_cnt)
    for (var i = 0; i < col_cnt; i++) {
        console.log('   ' + i)
        rows[0].getElementsByTagName("th")[i].getElementsByClassName("arrow_sort")[0].innerText = '▼'
    }
    var symbol = dir == "asc" ? '▲' : '▼'
    rows[0].getElementsByTagName("th")[column].getElementsByClassName("arrow_sort")[0].innerText = symbol
}
