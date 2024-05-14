// loads banner into a page
document.addEventListener("DOMContentLoaded", function() {
    const sidebarContainer = document.getElementById('banner-container');
    fetch('../components/banner.html')
        .then(response => response.text())
        .then(data => {
        sidebarContainer.innerHTML = data;

        // Show the toast after the banner has been loaded
        const toastEl = document.querySelector('.toast');
        if (toastEl) {
            const toast = new bootstrap.Toast(toastEl, {
                autohide: true,
                delay: 5000
            });
            toast.show();
        }
    })
    .catch(error => console.error('Failed to load the banner:', error));
});


// loads github button into a page
document.addEventListener("DOMContentLoaded", function() {
    const sidebarContainer = document.getElementById('github');
    fetch('../components/github_button.html')
        .then(response => response.text())
        .then(data => sidebarContainer.innerHTML = data);
});

// This script loads the sidebar into each page
document.addEventListener("DOMContentLoaded", function() {
    const sidebarContainer = document.getElementById('sidebar-container');
    fetch('../components/sidebar.html')
        .then(response => response.text())
        .then(data => sidebarContainer.innerHTML = data);
});

// This script loads the registration form into each page
document.addEventListener("DOMContentLoaded", function() {
    const sidebarContainer = document.getElementById('registration-button');
    fetch('../components/registration.html')
        .then(response => response.text())
        .then(data => sidebarContainer.innerHTML = data);
});
