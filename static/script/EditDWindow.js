
const element = document.querySelector(".showModalId");
const crossButton = document.querySelector("#crossBtn");
const closeButton = document.querySelector("#closeBtn");
const dialog = document.querySelector("#payment-approval__dialog");


var elements = document.getElementsByClassName("showModalId");
for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener("click", function () {
        var dialog = document.getElementById("payment-approval__dialog");
        dialog.showModal();
    });
}

crossButton.addEventListener("click", closeDialog);
function closeDialog() {
    dialog.close();
}
closeButton.addEventListener("click", closeDialog);
function closeDialog() {
    dialog.close();
}
