

function exportCSVExcel() {
	var tableElement = document.getElementById("payment-table");
	var sourceData = "data:text/csv;charset=utf-8,%EF%BB%BF";
	var sourceData = "data:text/csv;charset=utf-8,";
	var i = 0;
	sourceData += "\r\n";
	while (row = tableElement.rows[i]) {
	    var tmp = ''
		for (var j=0; j<tableElement.rows[0].cells.length; j++) {
		    tmp += row.cells[j].innerText + "\t";
//		    console.log(`--${row.cells[j].innerText}--`)

		}
		console.log(tmp)
		sourceData += tmp + "\r\n";
//		sourceData += ([
//			row.cells[0].innerText,
//			row.cells[1].innerText,
//			row.cells[2].innerText,
//			row.cells[3].innerText
//		]).join(",") + "\r\n";
        i++;

	}
//	console.log(sourceData)
	window.location.href = encodeURI(sourceData);
}