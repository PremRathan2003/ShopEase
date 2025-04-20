document.addEventListener("DOMContentLoaded", function () {
    
    // 1️⃣ Hover Event - Changes button color on hover
    const registerButton = document.querySelector(".login-btn");
    if (registerButton) {
        registerButton.addEventListener("mouseover", function () {
            registerButton.style.backgroundColor = "#28a745"; // Green color on hover
        });

        registerButton.addEventListener("mouseleave", function () {
            registerButton.style.backgroundColor = "#007BFF"; // Original color
        });
    }

    // 2️⃣ On Focus Event - Highlights input fields when user focuses
    const inputFields = document.querySelectorAll("input, textarea");
    inputFields.forEach(input => {
        input.addEventListener("focus", function () {
            input.style.border = "2px solid #007BFF"; // Blue border when focused
        });

        input.addEventListener("blur", function () {
            input.style.border = "1px solid #ccc"; // Restore default border
        });
    });

    // 3️⃣ Right Click Event - Custom Alert when right-clicking on the page
    document.addEventListener("contextmenu", function (event) {
        event.preventDefault(); // Prevents the default right-click menu
        alert("Right-click is disabled on this page for security reasons.");
    });

});
