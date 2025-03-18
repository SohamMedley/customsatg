def generate_cart_page():
    cart_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shopping Cart - CustomsATG</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
</head>
<body>
    <!-- Navigation -->
    <header class="navbar">
        <div class="container">
            <div class="navbar-content">
                <a href="{{ url_for('index') }}" class="logo">CustomsATG</a>
                
                <nav class="nav-desktop">
                    <ul>
                        <li><a href="{{ url_for('index') }}">Home</a></li>
                        <li><a href="{{ url_for('customize') }}">Customize T-Shirt</a></li>
                        <li><a href="{{ url_for('about') }}">About Us</a></li>
                        <li><a href="{{ url_for('contact') }}">Contact Us</a></li>
                    </ul>
                </nav>
                
                <div class="nav-actions">
                    <a href="{{ url_for('login') }}" class="btn-ghost">Login / Sign Up</a>
                    <a href="{{ url_for('cart') }}" class="btn-icon active">
                        <i class="fas fa-shopping-cart"></i>
                        <span class="cart-count">{{ cart|length }}</span>
                    </a>
                    <a href="{{ url_for('customize') }}" class="btn-primary">Start Designing</a>
                </div>
                
                <button class="menu-toggle" id="menuToggle">
                    <i class="fas fa-bars"></i>
                </button>
            </div>
            
            <!-- Mobile Menu -->
            <div class="mobile-menu" id="mobileMenu">
                <ul>
                    <li><a href="{{ url_for('index') }}">Home</a></li>
                    <li><a href="{{ url_for('customize') }}">Customize T-Shirt</a></li>
                    <li><a href="{{ url_for('about') }}">About Us</a></li>
                    <li><a href="{{ url_for('contact') }}">Contact Us</a></li>
                    <li><a href="{{ url_for('login') }}">Login / Sign Up</a></li>
                    <li><a href="{{ url_for('cart') }}">Cart ({{ cart|length }})</a></li>
                    <li><a href="{{ url_for('customize') }}" class="btn-primary">Start Designing</a></li>
                </ul>
            </div>
        </div>
    </header>

    <main>
        <section class="cart-section">
            <div class="container">
                <h1>Shopping Cart</h1>
                <p class="section-desc">Review your items and proceed to checkout</p>
                
                {% if cart|length > 0 %}
                <div class="cart-grid">
                    <!-- Cart Items -->
                    <div class="cart-items">
                        {% for item in cart %}
                        <div class="cart-item">
                            <div class="item-image">
                                <img src="{{ url_for('static', filename='img/tshirt-' + item.color + '.png') }}" alt="{{ item.color }} t-shirt">
                                <div class="item-design" style="left: {{ item.positionX }}%; top: {{ item.positionY }}%; transform: translate(-50%, -50%) scale({{ item.scale/100 }}) rotate({{ item.rotation }}deg);">
                                    <img src="{{ item.designPath }}" alt="Custom design">
                                </div>
                            </div>
                            <div class="item-details">
                                <h3>Custom T-Shirt</h3>
                                <p>Color: <span class="item-color">{{ item.color|capitalize }}</span></p>
                                <p>Size: <span class="item-size">{{ item.size }}</span></p>
                                <div class="item-quantity">
                                    <label>Quantity:</label>
                                    <div class="quantity-control">
                                        <button class="quantity-btn decrease-btn" data-id="{{ item.id }}">-</button>
                                        <input type="number" value="{{ item.quantity }}" min="1" class="quantity-input" data-id="{{ item.id }}">
                                        <button class="quantity-btn increase-btn" data-id="{{ item.id }}">+</button>
                                    </div>
                                </div>
                            </div>
                            <div class="item-price">
                                <p class="price">${{ "%.2f"|format(item.totalPrice) }}</p>
                                <button class="remove-item" data-id="{{ item.id }}">
                                    <i class="fas fa-trash"></i> Remove
                                </button>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    
                    <!-- Order Summary -->
                    <div class="order-summary-card">
                        <h2>Order Summary</h2>
                        
                        <div class="summary-items">
                            <div class="summary-item">
                                <span>Subtotal</span>
                                <span>${{ "%.2f"|format(cart|sum(attribute='totalPrice')) }}</span>
                            </div>
                            
                            <div class="summary-item">
                                <span>Shipping</span>
                                <span>$5.99</span>
                            </div>
                            
                            <div class="summary-item">
                                <span>Tax</span>
                                <span>${{ "%.2f"|format(cart|sum(attribute='totalPrice') * 0.08) }}</span>
                            </div>
                        </div>
                        
                        <div class="summary-total">
                            <span>Total</span>
                            <span>${{ "%.2f"|format(cart|sum(attribute='totalPrice') + 5.99 + (cart|sum(attribute='totalPrice') * 0.08)) }}</span>
                        </div>
                        
                        <button id="checkoutBtn" class="btn-primary full-width">Proceed to Checkout</button>
                        
                        <a href="{{ url_for('customize') }}" class="btn-outline full-width">Continue Shopping</a>
                    </div>
                </div>
                {% else %}
                <div class="empty-cart">
                    <div class="empty-cart-icon">
                        <i class="fas fa-shopping-cart"></i>
                    </div>
                    <h2>Your cart is empty</h2>
                    <p>Looks like you haven't added any items to your cart yet.</p>
                    <a href="{{ url_for('customize') }}" class="btn-primary">Start Designing</a>
                </div>
                {% endif %}
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h3>CustomsATG</h3>
                    <p>Express yourself with custom t-shirts that reflect your unique personality.</p>
                    <div class="social-links">
                        <a href="#"><i class="fab fa-facebook"></i></a>
                        <a href="#"><i class="fab fa-instagram"></i></a>
                        <a href="#"><i class="fab fa-twitter"></i></a>
                        <a href="#"><i class="fab fa-youtube"></i></a>
                    </div>
                </div>
                
                <div class="footer-col">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="{{ url_for('index') }}">Home</a></li>
                        <li><a href="{{ url_for('customize') }}">Customize T-Shirt</a></li>
                        <li><a href="{{ url_for('about') }}">About Us</a></li>
                        <li><a href="{{ url_for('contact') }}">Contact Us</a></li>
                    </ul>
                </div>
                
                <div class="footer-col">
                    <h3>Customer Service</h3>
                    <ul>
                        <li><a href="{{ url_for('faq') }}">FAQ</a></li>
                        <li><a href="{{ url_for('shipping') }}">Shipping & Returns</a></li>
                        <li><a href="{{ url_for('terms') }}">Terms & Conditions</a></li>
                        <li><a href="{{ url_for('privacy') }}">Privacy Policy</a></li>
                    </ul>
                </div>
                
                <div class="footer-col">
                    <h3>Contact Us</h3>
                    <address>
                        <p>123 Fashion Street</p>
                        <p>Design District, CA 90210</p>
                        <p>Email: info@customsatg.com</p>
                        <p>Phone: (123) 456-7890</p>
                    </address>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; <span id="currentYear">{{ current_year }}</span> CustomsATG. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    <script src="{{ url_for('static', filename='js/cart.js') }}"></script>
</body>
</html>
"""

    # Create templates directory if it doesn't exist
    import os
    os.makedirs('templates', exist_ok=True)
    
    # Write cart page to templates directory
    with open(os.path.join('templates', 'cart.html'), 'w', encoding='utf-8') as f:
        f.write(cart_html)
    
    print("Generated cart.html template")

if __name__ == '__main__':
    generate_cart_page()