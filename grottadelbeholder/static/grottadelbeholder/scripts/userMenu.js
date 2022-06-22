function showUserMenu() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function hideUserMenu() {
    if (!e.target.matches('.dropbtn')) {
        var myDropdown = document.getElementById("myDropdown");
        if (myDropdown.classList.contains('show')) {
            myDropdown.classList.remove('show');
        }
    }
}