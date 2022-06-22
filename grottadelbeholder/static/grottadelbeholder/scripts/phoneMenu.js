function showPhoneMenu() {
    let phoneMenuButton = document.getElementById("phoneMenuButton");
    let nav = document.getElementsByTagName("nav")[0];

    phoneMenuButton.innerText = "X"
    phoneMenuButton.onclick = function () {
        hidePhoneMenu()
    };

    nav.style.display = "inherit";
}

function hidePhoneMenu() {
    let phoneMenuButton = document.getElementById("phoneMenuButton");
    let nav = document.getElementsByTagName("nav")[0];

    phoneMenuButton.innerText = "="
    phoneMenuButton.onclick = function () {
        showPhoneMenu()
    };

    nav.style.display = "none";
}