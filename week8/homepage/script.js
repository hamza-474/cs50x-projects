document.addEventListener('DOMContentLoaded', function() {
    var year = document.querySelector('#year');
    if (year) {
        year.textContent = new Date().getFullYear();
    }
    var greeting = document.querySelector('#greeting');
    if (greeting) {
        var hour = new Date().getHours();
        if (hour < 12) {
            greeting.textContent = 'Good morning, and welcome to my site!';
        } else if (hour < 18) {
            greeting.textContent = 'Good afternoon, and welcome to my site!';
        } else {
            greeting.textContent = 'Good evening, and welcome to my site!';
        }
    }
    var toggle = document.querySelector('#theme-toggle');
    if (toggle) {
        toggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            if (document.body.classList.contains('dark-mode')) {
                toggle.textContent = 'Switch to Light Mode';
            } else {
                toggle.textContent = 'Switch to Dark Mode';
            }
        });
    }
    var form = document.querySelector('#contact-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            document.querySelector('#form-message').textContent = 'Thank you for your message! I will get back to you soon.';
            form.reset();
        });
    }
});
