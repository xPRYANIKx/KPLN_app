const dialog = document.querySelector("#payment-approval__dialog");
const cancelButton = document.querySelector("#cancel__edit_btn");
const crossButton = document.querySelector("#crossBtn");

cancelButton.addEventListener("click", closeDialog);
crossButton.addEventListener("click", closeDialog);

function closeDialog() {
    dialog.remove();
    location.reload();
}