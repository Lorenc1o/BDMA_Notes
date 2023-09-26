// scripts.js
document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('click', function() {
            const university = card.getAttribute('data-university');
            window.location.href = `./${university}.html`;  // Navigates to university-specific page
        });
    });
});

