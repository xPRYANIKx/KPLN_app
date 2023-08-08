function sortTable(column, type_col='str') {
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
        for (var i1=0; i1<rows[i].getElementsByTagName("td").length; i1++) {
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