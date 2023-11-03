let today = new Date();
let year = today.getFullYear();
document.getElementById("yearToday").textContent = year;

document.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
    }
});