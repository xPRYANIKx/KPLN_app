function validateInput() {
    const input = document.getElementById("responsible");
    const options = document.getElementById("responsible_name").children;

    let valid = false;
    for (let i = 0; i < options.length; i++) {
        if (options[i].value === input.value) {
            valid = true;
            break;
        }
    }

    if (valid) {
        input.setCustomValidity(""); // Clear any previous validation message
    } else {
        input.setCustomValidity("Не верное значение"); // Set custom validation message
    }
}