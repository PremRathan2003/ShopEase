// Function to display stored messages in the table
function displayMessages() {
    let tableBody = document.querySelector("#messagesTable tbody");
    tableBody.innerHTML = ""; // Clear previous table content

    let messages = JSON.parse(localStorage.getItem("messages")) || [];

    if (messages.length === 0) {
        let row = tableBody.insertRow();
        let cell = row.insertCell(0);
        cell.colSpan = 4; // Span across all columns
        cell.innerText = "No messages received.";
        return;
    }

    messages.forEach((msg, index) => {
        let row = tableBody.insertRow();
        row.insertCell(0).innerText = msg.name;
        row.insertCell(1).innerText = msg.email;
        row.insertCell(2).innerText = msg.message;

        let deleteCell = row.insertCell(3);
        let deleteButton = document.createElement("button");
        deleteButton.innerHTML = "🗑️";
        deleteButton.style.cursor = "pointer";
        deleteButton.style.backgroundColor = "#dc3545";
        deleteButton.style.color = "white";
        deleteButton.style.border = "none";
        deleteButton.style.padding = "6px 12px";
        deleteButton.style.borderRadius = "5px";
        deleteButton.style.transition = "all 0.3s ease";

        deleteButton.onmouseover = function () {
            deleteButton.style.backgroundColor = "#c82333";
        };
        deleteButton.onmouseleave = function () {
            deleteButton.style.backgroundColor = "#dc3545";
        };

        deleteButton.onclick = function () {
            if (confirm("Are you sure you want to delete this message?")) {
                removeMessage(index);
            }
        };

        deleteCell.appendChild(deleteButton);
    });
}

// Function to remove a message from localStorage and update the table
function removeMessage(index) {
    let messages = JSON.parse(localStorage.getItem("messages")) || [];
    messages.splice(index, 1);
    localStorage.setItem("messages", JSON.stringify(messages));
    displayMessages();
}

// Load stored messages automatically when the page loads
window.onload = displayMessages;
