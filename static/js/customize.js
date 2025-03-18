document.addEventListener('DOMContentLoaded', function() {
  // Mapping of color values to the exact file names in static/img/
  const tshirtImageMapping = {
    black: 'blackshirt.png',
    white: 'whiteshirt.png',
    gray: 'grayshirt.png'
    // add more mappings if needed
  };

  const tshirtImage = document.getElementById('tshirtImage');
  const summaryColor = document.getElementById('summaryColor');
  const colorOptions = document.querySelectorAll('input[name="tshirtColor"]');

  // Update the t-shirt image based on the selected color
  function updateTshirtImage() {
    const selectedColor = document.querySelector('input[name="tshirtColor"]:checked').value;
    const fileName = tshirtImageMapping[selectedColor] || 'default.png';
    tshirtImage.innerHTML = `<img src="/static/img/${fileName}" alt="${selectedColor} t-shirt">`;
    summaryColor.textContent = selectedColor;
  }

  updateTshirtImage();

  colorOptions.forEach(option => {
    option.addEventListener('change', updateTshirtImage);
  });

  // Handle design upload
  if (designUploadArea && designUpload) {
    designUploadArea.addEventListener('click', () => designUpload.click());
    designUpload.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          designThumbnail.src = e.target.result;
          designPreviewArea.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
      }
    });
  }

  if (removeDesign) {
    removeDesign.addEventListener('click', function() {
      designThumbnail.src = '/placeholder.svg';
      designPreviewArea.classList.add('hidden');
      designUpload.value = '';
    });
  }

  // Update order summary based on quantity
  function updateOrderSummary() {
    const quantity = parseInt(quantityInput.value);
    summaryQuantity.textContent = quantity;
    const total = (19.99 + 5.99) * quantity;
    summaryTotal.textContent = `$${total.toFixed(2)}`;
  }
  updateOrderSummary();

  decreaseQuantity.addEventListener('click', function() {
    let quantity = parseInt(quantityInput.value);
    if (quantity > 1) {
      quantity--;
      quantityInput.value = quantity;
      updateOrderSummary();
    }
  });

  increaseQuantity.addEventListener('click', function() {
    let quantity = parseInt(quantityInput.value);
    quantity++;
    quantityInput.value = quantity;
    updateOrderSummary();
  });

  quantityInput.addEventListener('change', updateOrderSummary);

  // Additional code for handling design position, scale, and rotation can be added here.
});
