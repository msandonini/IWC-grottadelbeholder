function checkPwd() {
    let pwdField = document.getElementById("newPassword");
    if (pwdField.textContent.trim() !== "") {
        document.getElementById("submitNewPwd").style.pointerEvents = "auto";
    }
    else {
        document.getElementById("submitNewPwd").style.pointerEvents = "none";
    }
}