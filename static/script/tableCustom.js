const crossButtonTC = document.querySelector("#crossBtnTC");
const dialogTC = document.querySelector("#tableCustom");


crossButtonTC.addEventListener("click", closeDialogTC);
function closeDialogTC() {
    dialogTC.close();
}

//$("td:nth-child(2)").hide()
var col_lst = [];

table = document.getElementById("payment-table");
cols = table.getElementsByTagName("tr")[0].getElementsByTagName("th");

for (var i=0; i<cols.length; i++) {
    var jj = cols[i].getElementsByTagName("div")[0].innerHTML.split('&nbsp;')[0];
    col_lst.push(jj)
}

var table_columns_list = document.getElementById('columns_list');

if (col_lst.length) {
    for (var i=0; i<col_lst.length; i++) {

        let newRow = document.createElement("tr");

        let newCell_1 = document.createElement("td");
        newCell_1.className = "ttdname"
        newCell_1.innerHTML = col_lst[i][0].toUpperCase() + col_lst[i].substring(1).toLowerCase();

        let newCell_2 = document.createElement("td");
        newCell_2.className = "ttdcbox";
        var newCell_2_input = document.createElement("input");
        newCell_2_input.type = "checkbox";
        newCell_2_input.checked = true;
        newCell_2.appendChild(newCell_2_input)

        newRow.appendChild(newCell_1);
        newRow.appendChild(newCell_2);
        table_columns_list.appendChild(newRow);
    }
}
else {
    table_columns_list.textContent = 0;
}


function tableCustomSave() {
    var table_custom2 = document.getElementById("columns_list").getElementsByTagName("tr");

    // Список скрываемых колонок
    hide_col_lst = [];
    show_col_lst = [];
    for (var i=0; i<table_custom2.length; i++) {
        row = table_custom2[i].getElementsByTagName("td");
        if (!row[1].getElementsByTagName("input")[0].checked) {
            hide_col_lst.push(i);
        }
        else {
            show_col_lst.push(i);
        }
    }

    // Список скрытых ранее столбцов
    table2 = document.getElementById("payment-table");
    rows2 = table2.getElementsByTagName("tr")[0].getElementsByTagName("th");
//    hide_col_lst2 = [];
    show_col_lst2 = [];

    for (var i=0; i<rows2.length; i++) {
        var jj = rows2[i].style.display;
        if (jj == 'none') {
            for (var s of show_col_lst) {
                i==s? show_col_lst2.push(i): 1;
            }
        }
    }

    if (hide_col_lst.length) {
        for (var i of hide_col_lst) {
            $(`#payment-table th:nth-child(${i+1})`).hide()
            $(`#payment-table td:nth-child(${i+1})`).hide()
        }
    }

    if (show_col_lst2.length) {
        for (var i of show_col_lst2) {
            $(`#payment-table th:nth-child(${i+1})`).show()
            $(`#payment-table td:nth-child(${i+1})`).show()
        }
    }

//    if (hide_col_lst.length || show_col_lst2.length) {
//        console.log("сохранение в БД");
//
//        var page_url = document.URL.substring(document.URL.lastIndexOf('/')+1);
//
//        fetch('/save_tab_settings', {
//                "headers": {
//                    'Content-Type': 'application/json'
//                },
//                "method": "POST",
//                "body": JSON.stringify({
//                    'page_url': page_url,
//                    'show_list': show_col_lst2,
//                    'hide_list': hide_col_lst
//                })
//            })
//                .then(response => response.json())
//                .then(data => {
//                    if (data.status === 'success') {
//                        console.log(data)
//
//
//
//                }
//                else if (data.status === 'error') {
//                    alert(data.description)
//                }
//                else {
//                    window.location.href = `/${page_url}`;
//                }
//            })
//            .catch(error => {
//                console.error('Error:', error);
//            });
//
//
//    }


}
