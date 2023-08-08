document.addEventListener("DOMContentLoaded", function () {
    var menu = document.getElementById("menu");
    var image = document.getElementById("menuImage");

    document.addEventListener("click", (event) => {
        const menuClick = event.target == menu || menu.contains(event.target)
        const menuButtonClick = event.target == image
        if (!menuClick && !menuButtonClick) {
            menu.style.display = "none";
            image.src = 'static/img/menu.png'
        }
    });

    image.addEventListener("click", function () {
        var isMenuVisible = menu.style.display === "flex";
        if (isMenuVisible) {
            menu.style.display = "none";
            image.src = 'static/img/menu.png'
        } else {
            menu.style.display = "flex";
            image.src = 'static/img/menu_end.png'
        }
    });
});