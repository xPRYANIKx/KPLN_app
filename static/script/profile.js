$(document).ready(function () {
    const toggleNewPassword = document.querySelector("#toggleNewPassword");
    const new_password = document.querySelector("#new_password");

    const toggleConfPassword = document.querySelector("#toggleConfPassword");
    const confirm_password = document.querySelector("#confirm_password");

    toggleNewPassword.addEventListener("click", function () {
        // toggle the type attribute
        const type = new_password.getAttribute("type") === "password" ? "text" : "password";
        new_password.setAttribute("type", type);

        // toggle the icon
        this.classList.toggle("bi-eye");
    });

    toggleConfPassword.addEventListener("click", function () {
        // toggle the type attribute
        const type = confirm_password.getAttribute("type") === "password" ? "text" : "password";
        confirm_password.setAttribute("type", type);

        // toggle the icon
        this.classList.toggle("bi-eye");
    });
});

function checkPasswordCompliant() {

    const new_password = document.querySelector("#new_password").value;
    const confirm_password = document.querySelector("#confirm_password").value;
    console.log(new_password)
    console.log(confirm_password)
//    String password = this;
//    bool hasUppercase = password.contains(RegExp(r'[A-Z]'));
//    bool hasLowercase = password.contains(RegExp(r'[a-z]'));
//    bool hasDigits = password.contains(RegExp(r'[0-9]'));
//    bool hasSpecialCharacters = password.contains(RegExp(r'[!@#$%^&*(),.?":{}|<>]'));
//    bool hasMinLength = password.length > 8;
//
//    return hasUppercase && hasLowercase && hasDigits && hasSpecialCharacters && hasMinLength;

}
