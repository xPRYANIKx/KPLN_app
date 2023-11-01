function filterTable() {
    var filter_input = document.querySelectorAll('[id*="filter-input-"]');
    var filterValsList = []; // Значения фильтров
    var filterCol = []; // Список фильтруемых столбцов

    for (var i=0; i<filter_input.length; i++) {
        filterValsList.push(filter_input[i].value.toUpperCase());
        filter_input[i].value? filterCol.push(i): 1;
    }

    var cntColFilter = filterCol.length; // Количество столбцов у которых задан фильтр

    var table = document.getElementById("payment-table");
    var rows = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those that don't match the filter
    for (var i = 1; i < rows.length; i++) {
        var cellsVal = [];
        var matchCounter = 0;
        for (j of filterCol) {
            var cellVal = rows[i].getElementsByTagName("td")[j].textContent.toUpperCase();
            var filterVal = filterValsList[j];

            console.log(`  ${i}  ${cellVal} / ${filterVal}`)

            matchCounter += cellVal.includes(filterVal)
        }
        if (cntColFilter == matchCounter) {
            rows[i].style.display = "";
        }
        else {
            rows[i].style.display = "none";
        }
    }
}
