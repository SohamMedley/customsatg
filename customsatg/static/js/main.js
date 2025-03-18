document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  const menuToggle = document.getElementById('menuToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  
  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', function() {
      mobileMenu.classList.toggle('active');
    });
  }
  
  // Set current year in footer
  const currentYearElements = document.querySelectorAll('#currentYear');
  const currentYear = new Date().getFullYear();
  
  currentYearElements.forEach(function(element) {
    element.textContent = currentYear;
  });
  
  // Placeholder for cart count update (implement as needed)
  updateCartCount();
});

function updateCartCount() {
  // For now, this simply logs the action.
  // In production, fetch the count from the server if needed.
  console.log("Updating cart count...");
}
