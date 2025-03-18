document.addEventListener('DOMContentLoaded', function() {
  // Handle tab switching for login/signup
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const tabId = this.getAttribute('data-tab');
      // Remove active classes
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));
      // Activate current tab and pane
      this.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    });
  });

  // Login form submission
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const email = document.getElementById('loginEmail').value;
      const password = document.getElementById('loginPassword').value;
      if (!email || !password) {
        alert('Please fill in all fields');
        return;
      }
      fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          window.location.href = '/';
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

  // Signup form submission
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const firstName = document.getElementById('firstName').value;
      const lastName = document.getElementById('lastName').value;
      const email = document.getElementById('signupEmail').value;
      const password = document.getElementById('signupPassword').value;
      const confirmPassword = document.getElementById('confirmPassword').value;
      if (!firstName || !lastName || !email || !password || !confirmPassword) {
        alert('Please fill in all fields');
        return;
      }
      if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
      }
      fetch('/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ firstName, lastName, email, password, confirmPassword })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          window.location.href = '/';
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
});
