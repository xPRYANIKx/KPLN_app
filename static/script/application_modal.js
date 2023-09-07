function applicationModal() {
  // Send an AJAX request to the server to get the modal HTML
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/modal', true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      // Create a new div element and set its innerHTML to the modal HTML
      var modalDiv = document.createElement('div');
      modalDiv.innerHTML = xhr.responseText;

      // Append the modal div to the document body
      document.body.appendChild(modalDiv);

      // Add event listener to the submit form
      var submitForm = document.getElementById('submit-form');
      submitForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Get the data from the form input
        var data = submitForm.elements['data'].value;

        // Send an AJAX request to the server to process the data
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/get_modal_payment', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
          if (xhr.readyState === 4 && xhr.status === 200) {
            // Handle the server response here
          }
        };
        xhr.send(JSON.stringify({ data: data }));

        // Remove the modal window
        document.body.removeChild(modalDiv);
      });
    }
  };
  xhr.send();
});
