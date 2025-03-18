document.addEventListener('DOMContentLoaded', function() {
  const contactForm = document.getElementById('contactForm');
  const formSuccess = document.getElementById('formSuccess');
  const sendAnother = document.getElementById('sendAnother');

  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const firstName = document.getElementById('firstName').value;
      const lastName = document.getElementById('lastName').value;
      const email = document.getElementById('email').value;
      const phone = document.getElementById('phone').value;
      const subject = document.getElementById('subject').value;
      const message = document.getElementById('message').value;
      if (!firstName || !lastName || !email || !subject || !message) {
        alert('Please fill in all required fields');
        return;
      }
      fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ firstName, lastName, email, phone, subject, message })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          contactForm.classList.add('hidden');
          formSuccess.classList.remove('hidden');
        } else {
          alert(data.message);
        }
      })
      .catch(err => {
        console.error(err);
        alert('An error occurred. Please try again.');
      });
    });
  }

  if (sendAnother) {
    sendAnother.addEventListener('click', function() {
      formSuccess.classList.add('hidden');
      contactForm.classList.remove('hidden');
      contactForm.reset();
    });
  }
});
