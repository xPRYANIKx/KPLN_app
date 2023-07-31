function sortTable(column) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("payment-table");
    switching = true;
    // Set the sorting direction to ascending
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.getElementsByTagName("tr");
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[column];
            y = rows[i + 1].getElementsByTagName("td")[column];
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            for (i = 1; i < (rows.length - 1); i++) {
                var new_abbr = rows[i].getElementsByTagName("td")[0].getElementsByTagName("input")[0].getAttribute("value").split('-***-')
                var new_abbr = i + '-***-' + new_abbr[1]
                                      rows[i].getElementsByTagName("td")[0].getElementsByTagName("input")[0].setAttribute("value", new_abbr)
                console.log('i =', i, rows[i].getElementsByTagName("td")[0].getElementsByTagName("input")[0].getAttribute("value"), rows[i]);
            }
            console.log(2);
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}