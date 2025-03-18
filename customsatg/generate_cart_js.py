def generate_cart_js():
    cart_js = """
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const decreaseBtns = document.querySelectorAll('.decrease-btn');
    const increaseBtns = document.querySelectorAll('.increase-btn');
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const removeItemBtns = document.querySelectorAll('.remove-item');
    const checkoutBtn = document.getElementById('checkoutBtn');
    
    // Decrease quantity
    decreaseBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const input = document.querySelector(`.quantity-input[data-id="${id}"]`);
            let quantity = parseInt(input.value);
            
            if (quantity > 1) {
                quantity--;
                input.value = quantity;
                updateCartItem(id, quantity);
            }
        });
    });
    
    // Increase quantity
    increaseBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const input = document.querySelector(`.quantity-input[data-id="${id}"]`);
            let quantity = parseInt(input.value);
            
            quantity++;
            input.value = quantity;
            updateCartItem(id, quantity);
        });
    });
    
    // Quantity input change
    quantityInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const id = this.getAttribute('data-id');
            let quantity = parseInt(this.value);
            
            if (quantity < 1) {
                quantity = 1;
                this.value = quantity;
            }
            
            updateCartItem(id, quantity);
        });
    });
    
    // Remove item
    removeItemBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            removeCartItem(id);
        });
    });
    
    // Checkout
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            // In a real app, this would redirect to a checkout page
            alert('Checkout functionality would be implemented here');
            // window.location.href = '/checkout';
        });
    }
    
    // Update cart item
    function updateCartItem(id, quantity) {
        fetch('/api/update-cart-item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: id,
                quantity: quantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reload the page to reflect changes
                window.location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }
    
    // Remove cart item
    function removeCartItem(id) {
        fetch('/api/remove-cart-item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: id
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reload the page to reflect changes
                window.location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }
});
"""

    # Create static/js directory if it doesn't exist
    import os
    os.makedirs('static/js', exist_ok=True)
    
    # Write cart.js to static/js directory
    with open(os.path.join('static/js', 'cart.js'), 'w', encoding='utf-8') as f:
        f.write(cart_js)
    
    print("Generated cart.js file")

if __name__ == '__main__':
    generate_cart_js()