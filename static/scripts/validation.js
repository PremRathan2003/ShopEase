// Function to validate the registration form
function validateRegistrationForm() {
    // Retrieve form values
    let firstName = document.getElementById("firstName").value.trim();
    let lastName = document.getElementById("lastName").value.trim();
    let email = document.getElementById("email").value.trim();
    let dob = document.getElementById("dob").value;
    let gender = document.getElementById("gender").value;
    let phone = document.getElementById("phone").value.trim();
    let address = document.getElementById("address").value.trim();
    let zipcode = document.getElementById("zipcode").value.trim();
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;
    let terms = document.getElementById("terms");

    // Regular Expressions
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    const phonePattern = /^(?:\+353|0)(?:[1-9]\d{0,1})\s?\d{3}\s?\d{4}$/;
    const zipPattern = /^[a-zA-Z0-9]{4,10}$/;
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

    // Validation Checks
    if (!firstName || !lastName || !email || !dob || !gender || !phone || !address || !zipcode || !password || !confirmPassword) {
        alert("Please fill in all required fields.");
        return false;
    }

    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

    if (!phonePattern.test(phone)) {
        alert("Please enter a valid phone number (e.g., 0871234567 or +353871234567).");
        return false;
    }

    if (!zipPattern.test(zipcode)) {
        alert("Please enter a valid postal code.");
        return false;
    }

    

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return false;
    }

    if (!terms.checked) {
        alert("You must agree to the Terms and Conditions before registering.");
        return false;
    }

    // Store user data in LocalStorage
    let userData = {
        firstName,
        lastName,
        email,
        dob,
        gender,
        phone,
        address,
        zipcode,
        password
    };

    let storedData = JSON.parse(localStorage.getItem("formData")) || [];
    storedData.push(userData);
    localStorage.setItem("formData", JSON.stringify(storedData));

    

    return true; // Prevent form from reloading the page
}

// Function to display stored user data in the table
function displayStoredData() {
    let tableBody = document.querySelector("#dataTable tbody");
    tableBody.innerHTML = ""; // Clear previous data

    let storedData = JSON.parse(localStorage.getItem("formData")) || [];

    if (storedData.length === 0) {
        let row = tableBody.insertRow();
        let cell = row.insertCell(0);
        cell.colSpan = 9; // Span across all columns
        cell.innerText = "No users found..!";
        return;
    }

    storedData.forEach((data, index) => {
        let row = tableBody.insertRow();
        row.insertCell(0).innerText = data.firstName;
        row.insertCell(1).innerText = data.lastName;
        row.insertCell(2).innerText = data.email;
        row.insertCell(3).innerText = data.dob;
        row.insertCell(4).innerText = data.phone;
        row.insertCell(5).innerText = data.address;
        row.insertCell(6).innerText = data.zipcode;

        // Delete Button
        let deleteCell = row.insertCell(7);
        let deleteButton = document.createElement("button");
        deleteButton.innerHTML = "🗑️";
        deleteButton.style.cursor = "pointer";
        deleteButton.style.backgroundColor = "#dc3545";
        deleteButton.style.color = "white";
        deleteButton.style.border = "none";
        deleteButton.style.padding = "6px 12px";
        deleteButton.style.borderRadius = "5px";
        deleteButton.style.transition = "all 0.3s";

        deleteButton.onmouseover = function () {
            deleteButton.style.backgroundColor = "#c82333";
        };
        deleteButton.onmouseleave = function () {
            deleteButton.style.backgroundColor = "#dc3545";
        };

        deleteButton.onclick = function () {
            if (confirm("Are you sure you want to delete this user?")) {
                removeUser(index);
            }
        };

        deleteCell.appendChild(deleteButton);
    });
}

// Function to remove a user from localStorage and update the table
function removeUser(index) {
    let storedData = JSON.parse(localStorage.getItem("formData")) || [];
    storedData.splice(index, 1);
    localStorage.setItem("formData", JSON.stringify(storedData));
    displayStoredData();
}

// Function to toggle visibility of the user data table
function toggleUserTable() {
    const table = document.getElementById("usersTable");
    table.style.display = table.style.display === "none" ? "block" : "none";
}

// Load stored user data automatically when the page loads
window.onload = displayStoredData;
