function submitForm() {
    let form = document.getElementById("loginForm");

    let messageDiv = document.getElementById("messageDiv");
    let messageP = document.getElementById("message");

    let message = ""

    try {
        let email = document.getElementById("emailField").value.trim();

        if (email === "") {
            message = "Inserire la mail"
        }
        else if (email.search("@") < 1 || email.search("\\.") < 0) {
            message = "Inserire una mail valida"
        }
    } catch (error) {}
    if (document.getElementById("userField").value.trim() === "" && message === "") {
        message = "Inserire il nome utente";
    }
    else if (document.getElementById("pwdField").value.trim() === "" && message === "") {
        message = "Inserire la password";
    }


    if (message === "") {
        form.submit();
    }
    else {
        messageP.innerText = message;
        messageDiv.style.visibility = "visible"
    }

}