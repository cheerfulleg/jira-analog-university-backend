    let myInput = document.getElementById("password")
    let length = document.getElementById("length");
    let submitBtn = document.getElementById("submit")

    myInput.onkeyup = function () {

        if (myInput.value.length >= 8) {
            length.classList.remove("invalid");
            length.classList.add("valid");
            submitBtn.disabled = false

        } else {
            submitBtn.disabled = true
            length.classList.remove("valid");
            length.classList.add("invalid");
        }
    }