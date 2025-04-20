// Get the button and menu elements
const menuToggleBtn = document.getElementById('menuToggleBtn'); // Button to open the menu
const closeMenuBtn = document.getElementById('closeMenuBtn');   // Button to close the menu
const dynamicMenu = document.getElementById('dynamicMenu');     // The menu itself

// Function to open the menu with a smooth animation
function openMenu() {
    // Initially hide and slightly move the menu up
    dynamicMenu.style.opacity = "0"; 
    dynamicMenu.style.transform = "translateY(-10px)"; 

    // Add the 'open' class to make the menu visible
    dynamicMenu.classList.add("open");

    // Use a slight delay before making it fully visible for a smooth effect
    setTimeout(() => {
        dynamicMenu.style.opacity = "1";
        dynamicMenu.style.transform = "translateY(0)";
    }, 50);
}

// Function to close the menu with a fade-out effect
function closeMenu() {
    // Ensure menu is visible before starting animation
    dynamicMenu.style.opacity = "1";
    dynamicMenu.style.transform = "translateY(0)";

    // Start the fade-out animation
    setTimeout(() => {
        dynamicMenu.style.opacity = "0"; 
        dynamicMenu.style.transform = "translateY(-10px)";

        // After the animation, remove the 'open' class to fully hide the menu
        setTimeout(() => dynamicMenu.classList.remove("open"), 300);
    }, 50);
}

// Event: Open menu when the button is clicked
menuToggleBtn.addEventListener('click', openMenu);

// Event: Close menu when the close button is clicked
closeMenuBtn.addEventListener('click', closeMenu);

// Event: Close menu when clicking outside of it
document.addEventListener('click', function (event) {
    // Ensure the click is outside the menu and not on the toggle button
    if (!dynamicMenu.contains(event.target) && event.target !== menuToggleBtn) {
        closeMenu();
    }
});

// Event: Open menu when hovering over the toggle button
menuToggleBtn.addEventListener('mouseover', openMenu);

// Event: Close menu when the mouse leaves the menu area
dynamicMenu.addEventListener('mouseleave', closeMenu);
