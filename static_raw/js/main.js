"use strict";

console.log("js works");

// close messages button
const closeButtons = document.querySelectorAll(".close");

closeButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        let message = this.closest(".message");

        if (message) {
            message.parentNode.removeChild(message);
        }
    });
});


// confirm password
const deleteAccountButton = document.getElementById("delete-account");
const changeDataButton = document.getElementById("change-data");

if (deleteAccountButton) {
    deleteAccountButton.addEventListener("click", function () {
        const promptText = "Enter password to delete account:";
        const passwordInput = "password-input-2";
        confirmPassword(promptText, passwordInput);
    });
}

if (changeDataButton) {
    changeDataButton.addEventListener("click", function () {
        const promptText = "Enter password to save changes:";
        const passwordInput = "password-input-1";
        confirmPassword(promptText, passwordInput);
    });
}

function confirmPassword(promptText, passwordInput) {
    let password = prompt(promptText);
    console.log(password);
    console.log(passwordInput);
    if (password !== null) {
        const inputElement = document.getElementById(passwordInput);
        if (inputElement) {
            inputElement.value = password;
        } else {
            console.error(`Element with id '${passwordInput}' not found.`);
        }
    }
}
