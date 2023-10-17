const verificationDialog = document.querySelector("#verification__dialog");
const closeButtonVerification = document.querySelector("#verification__dialog_cancel");

closeButtonVerification.addEventListener("click", closeVerificationDialog);
function closeVerificationDialog() {
    verificationDialog.close();
}

