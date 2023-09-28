function getModal2(paymentId = null) {
    var dataToUpdate = {
        paymentId: paymentId,
        newPaymentStatus: 'Completed'
    };

    // Send an AJAX request to the Flask route
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_payment', true);
    //    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Handle the response here
            var updatedData = JSON.parse(xhr.responseText);
            console.log(updatedData)

            // Update the window with the new data
            // Название карточки
            document.getElementById('card_title').innerText = updatedData.payment[5];

            // Наименование платежа
            document.getElementById('basis_of_payment').innerText = updatedData.payment[6];

            // Ответственный
            var selectElement = document.getElementById('responsible')
            selectElement.innerHTML = "";
            // Loop through the new list
            for (var i = 0; i < updatedData.responsible.length; i++) {
                // Create a new option element
                var option = document.createElement("option");
                // Set the value and text of the option
                option.value = updatedData.responsible[i][0];
                option.text = updatedData.responsible[i][1] + ' ' + updatedData.responsible[i][2];
                // Append the option to the select element
                selectElement.appendChild(option);
            }
            document.getElementById('responsible').value = updatedData.payment[7]

            // Тип заявки
            var selectElement = document.getElementById('cost_items')
            selectElement.innerHTML = "";
            // Loop through the new list
            for (var i = 0; i < updatedData.cost_items.length; i++) {
                // Create a new option element
                console.log(updatedData.cost_items[i][0], updatedData.cost_items[i][1], updatedData.cost_items[i][2])
                var optgroup = document.createElement("optgroup");
                for (var i2 = 0; i2 < updatedData.cost_items[i].length; i2++) {
                    var option = document.createElement("option");
                    // Set the value and text of the option
                    option.value = updatedData.cost_items[i][0];
                    option.text = updatedData.cost_items[i][1] + ' ' + updatedData.responsible[i][2];
                    // Append the option to the select element
                    selectElement.appendChild(option);
                }
                document.getElementById('cost_items').value = updatedData.payment[9] + ' ' + updatedData.payment[8]
                selectElement.selectedIndex = updatedData.payment[7]


                //            document.getElementById('responsible').innerText = updatedData.payment[6];
                console.log(updatedData.payment[5]);
                console.log(updatedData.payment);
            }
        };

        xhr.send(JSON.stringify(dataToUpdate));

    }
}