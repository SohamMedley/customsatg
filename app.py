from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime
import re
import uuid

app = Flask(__name__)
app.secret_key = 'customsatg_secret_key'  # For session management
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mock database (in a real app, use a proper database)
USERS_DB_FILE = 'users.json'
DESIGNS_DB_FILE = 'designs.json'
ORDERS_DB_FILE = 'orders.json'
MESSAGES_DB_FILE = 'messages.json'

def load_json_db(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_json_db(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize DB files if they don't exist
if not os.path.exists(USERS_DB_FILE):
    save_json_db([], USERS_DB_FILE)
if not os.path.exists(DESIGNS_DB_FILE):
    save_json_db([], DESIGNS_DB_FILE)
if not os.path.exists(ORDERS_DB_FILE):
    save_json_db([], ORDERS_DB_FILE)
if not os.path.exists(MESSAGES_DB_FILE):
    save_json_db([], MESSAGES_DB_FILE)

# Helper functions
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def get_user_by_email(email):
    users = load_json_db(USERS_DB_FILE)
    for user in users:
        if user['email'] == email:
            return user
    return None

# Routes
@app.route('/')
def index():
    return render_template('index.html', current_year=datetime.now().year)

@app.route('/customize')
def customize():
    return render_template('customize.html', current_year=datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html', current_year=datetime.now().year)

@app.route('/contact')
def contact():
    return render_template('contact.html', current_year=datetime.now().year)

@app.route('/login')
def login():
    return render_template('login.html', current_year=datetime.now().year)

@app.route('/cart')
def cart():
    # Get cart from session or initialize empty cart
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart, current_year=datetime.now().year)

@app.route('/faq')
def faq():
    return render_template('faq.html', current_year=datetime.now().year)

@app.route('/shipping')
def shipping():
    return render_template('shipping.html', current_year=datetime.now().year)

@app.route('/terms')
def terms():
    return render_template('terms.html', current_year=datetime.now().year)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', current_year=datetime.now().year)

# API Endpoints
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    user = get_user_by_email(email)
    if not user or user['password'] != password:  # In production, use proper password hashing
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    # Set user in session
    session['user'] = {
        'id': user['id'],
        'email': user['email'],
        'firstName': user['firstName'],
        'lastName': user['lastName']
    }
    
    return jsonify({'success': True, 'message': 'Login successful'})

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')
    
    # Validation
    if not all([first_name, last_name, email, password, confirm_password]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    if not is_valid_email(email):
        return jsonify({'success': False, 'message': 'Invalid email format'}), 400
    
    if password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
    
    if len(password) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters'}), 400
    
    # Check if user already exists
    if get_user_by_email(email):
        return jsonify({'success': False, 'message': 'Email already registered'}), 400
    
    # Create new user
    users = load_json_db(USERS_DB_FILE)
    new_user = {
        'id': str(uuid.uuid4()),
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'password': password,  # In production, hash the password
        'createdAt': datetime.now().isoformat()
    }
    users.append(new_user)
    save_json_db(users, USERS_DB_FILE)
    
    # Set user in session
    session['user'] = {
        'id': new_user['id'],
        'email': new_user['email'],
        'firstName': new_user['firstName'],
        'lastName': new_user['lastName']
    }
    
    return jsonify({'success': True, 'message': 'Account created successfully'})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    phone = data.get('phone', '')
    subject = data.get('subject')
    message = data.get('message')
    
    # Validation
    if not all([first_name, last_name, email, subject, message]):
        return jsonify({'success': False, 'message': 'Required fields are missing'}), 400
    
    if not is_valid_email(email):
        return jsonify({'success': False, 'message': 'Invalid email format'}), 400
    
    # Save message
    messages = load_json_db(MESSAGES_DB_FILE)
    new_message = {
        'id': str(uuid.uuid4()),
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'phone': phone,
        'subject': subject,
        'message': message,
        'createdAt': datetime.now().isoformat(),
        'read': False
    }
    messages.append(new_message)
    save_json_db(messages, MESSAGES_DB_FILE)
    
    # In a real app, you might send an email notification here
    
    return jsonify({'success': True, 'message': 'Message sent successfully'})

@app.route('/api/upload-design', methods=['POST'])
def api_upload_design():
    if 'design' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['design']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid duplicates
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Return the path to the uploaded file
        return jsonify({
            'success': True, 
            'message': 'Design uploaded successfully',
            'filePath': f"/static/uploads/{filename}"
        })

@app.route('/api/add-to-cart', methods=['POST'])
def api_add_to_cart():
    data = request.json
    color = data.get('color')
    size = data.get('size')
    quantity = data.get('quantity', 1)
    design_path = data.get('designPath')
    position_x = data.get('positionX', 50)
    position_y = data.get('positionY', 30)
    scale = data.get('scale', 100)
    rotation = data.get('rotation', 0)
    
    # Validation
    if not all([color, size, design_path]):
        return jsonify({'success': False, 'message': 'Required fields are missing'}), 400
    
    # Get cart from session or initialize empty cart
    cart = session.get('cart', [])
    
    # Add item to cart
    cart_item = {
        'id': str(uuid.uuid4()),
        'color': color,
        'size': size,
        'quantity': quantity,
        'designPath': design_path,
        'positionX': position_x,
        'positionY': position_y,
        'scale': scale,
        'rotation': rotation,
        'price': 19.99,  # Base price
        'printPrice': 5.99,  # Print price
        'totalPrice': (19.99 + 5.99) * quantity
    }
    cart.append(cart_item)
    
    # Update cart in session
    session['cart'] = cart
    
    return jsonify({
        'success': True, 
        'message': 'Item added to cart',
        'cartCount': len(cart)
    })

# JavaScript files
@app.route('/js/main.js')
def main_js():
    js_code = """
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
        
        // Update cart count from session if available
        updateCartCount();
    });

    function updateCartCount() {
        // In a real app, this would fetch from the server
        // For now, we'll just use a placeholder
        fetch('/api/cart-count')
            .then(response => response.json())
            .then(data => {
                const cartCountElements = document.querySelectorAll('.cart-count');
                cartCountElements.forEach(function(element) {
                    element.textContent = data.count;
                });
            })
            .catch(error => console.error('Error fetching cart count:', error));
    }
    """
    return app.response_class(js_code, mimetype='application/javascript')

@app.route('/js/login.js')
def login_js():
    js_code = """
    document.addEventListener('DOMContentLoaded', function() {
        // Tab switching
        const tabBtns = document.querySelectorAll('.tab-btn');
        const tabPanes = document.querySelectorAll('.tab-pane');
        
        tabBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');
                
                // Remove active class from all buttons and panes
                tabBtns.forEach(function(btn) {
                    btn.classList.remove('active');
                });
                
                tabPanes.forEach(function(pane) {
                    pane.classList.remove('active');
                });
                
                // Add active class to current button and pane
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
                
                // Validate form
                if (!email || !password) {
                    alert('Please fill in all fields');
                    return;
                }
                
                // Send login request
                fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = '/';
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
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
                
                // Validate form
                if (!firstName || !lastName || !email || !password || !confirmPassword) {
                    alert('Please fill in all fields');
                    return;
                }
                
                if (password !== confirmPassword) {
                    alert('Passwords do not match');
                    return;
                }
                
                // Send signup request
                fetch('/api/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        firstName: firstName,
                        lastName: lastName,
                        email: email,
                        password: password,
                        confirmPassword: confirmPassword
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = '/';
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
            });
        }
    });
    """
    return app.response_class(js_code, mimetype='application/javascript')

@app.route('/js/contact.js')
def contact_js():
    js_code = """
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
                
                // Validate form
                if (!firstName || !lastName || !email || !subject || !message) {
                    alert('Please fill in all required fields');
                    return;
                }
                
                // Send contact request
                fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        firstName: firstName,
                        lastName: lastName,
                        email: email,
                        phone: phone,
                        subject: subject,
                        message: message
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        contactForm.classList.add('hidden');
                        formSuccess.classList.remove('hidden');
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
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
    """
    return app.response_class(js_code, mimetype='application/javascript')

@app.route('/js/customize.js')
def customize_js():
    js_code = """
    document.addEventListener('DOMContentLoaded', function() {
        // Elements
        const tshirtImage = document.getElementById('tshirtImage');
        const designPreview = document.getElementById('designPreview');
        const designUploadArea = document.getElementById('designUploadArea');
        const designUpload = document.getElementById('designUpload');
        const designPreviewArea = document.getElementById('designPreviewArea');
        const designThumbnail = document.getElementById('designThumbnail');
        const removeDesign = document.getElementById('removeDesign');
        const checkoutBtn = document.getElementById('checkoutBtn');
        
        // Controls
        const positionX = document.getElementById('positionX');
        const positionY = document.getElementById('positionY');
        const designScale = document.getElementById('designScale');
        const designRotation = document.getElementById('designRotation');
        
        // T-shirt options
        const colorOptions = document.querySelectorAll('input[name="tshirtColor"]');
        const sizeSelect = document.getElementById('size');
        const quantityInput = document.getElementById('quantity');
        const decreaseQuantity = document.getElementById('decreaseQuantity');
        const increaseQuantity = document.getElementById('increaseQuantity');
        
        // Summary elements
        const summaryColor = document.getElementById('summaryColor');
        const summarySize = document.getElementById('summarySize');
        const summaryQuantity = document.getElementById('summaryQuantity');
        const summaryTotal = document.getElementById('summaryTotal');
        
        // Variables
        let designPath = null;
        const basePrice = 19.99;
        const printPrice = 5.99;
        
        // Initialize T-shirt image
        function updateTshirtImage() {
            const selectedColor = document.querySelector('input[name="tshirtColor"]:checked').value;
            tshirtImage.innerHTML = `<img src="/static/img/tshirt-${selectedColor}.png" alt="${selectedColor} t-shirt">`;
            
            if (summaryColor) {
                summaryColor.textContent = selectedColor;
            }
        }
        
        // Initialize with default color
        if (tshirtImage) {
            updateTshirtImage();
        }
        
        // Color selection
        colorOptions.forEach(function(option) {
            option.addEventListener('change', updateTshirtImage);
        });
        
        // Size selection
        if (sizeSelect) {
            sizeSelect.addEventListener('change', function() {
                if (summarySize) {
                    summarySize.textContent = this.value;
                }
            });
        }
        
        // Quantity controls
        if (decreaseQuantity && quantityInput && increaseQuantity) {
            decreaseQuantity.addEventListener('click', function() {
                let quantity = parseInt(quantityInput.value);
                if (quantity > 1) {
                    quantity--;
                    quantityInput.value = quantity;
                    updateSummary();
                }
            });
            
            increaseQuantity.addEventListener('click', function() {
                let quantity = parseInt(quantityInput.value);
                quantity++;
                quantityInput.value = quantity;
                updateSummary();
            });
            
            quantityInput.addEventListener('change', function() {
                let quantity = parseInt(this.value);
                if (quantity < 1) {
                    quantity = 1;
                    this.value = quantity;
                }
                updateSummary();
            });
        }
        
        // Update summary
        function updateSummary() {
            if (summaryQuantity && summaryTotal) {
                const quantity = parseInt(quantityInput.value);
                summaryQuantity.textContent = quantity;
                
                const total = (basePrice + printPrice) * quantity;
                summaryTotal.textContent = '$' + total.toFixed(2);
            }
        }
        
        // Design upload
        if (designUploadArea && designUpload) {
            designUploadArea.addEventListener('click', function() {
                designUpload.click();
            });
            
            designUpload.addEventListener('change', function(e) {
                const file = e.target.files[0];
                
                if (file) {
                    const formData = new FormData();
                    formData.append('design', file);
                    
                    fetch('/api/upload-design', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            designPath = data.filePath;
                            
                            // Show design preview
                            designPreview.innerHTML = `<img src="${designPath}" alt="Your design">`;
                            designPreview.style.display = 'block';
                            
                            // Show thumbnail
                            designThumbnail.src = designPath;
                            designUploadArea.classList.add('hidden');
                            designPreviewArea.classList.remove('hidden');
                            
                            // Enable checkout button
                            if (checkoutBtn) {
                                checkoutBtn.disabled = false;
                            }
                            
                            // Update design position
                            updateDesignPosition();
                        } else {
                            alert(data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('An error occurred while uploading your design. Please try again.');
                    });
                }
            });
        }
        
        // Remove design
        if (removeDesign) {
            removeDesign.addEventListener('click', function() {
                designPath = null;
                designPreview.innerHTML = '';
                designPreview.style.display = 'none';
                designUploadArea.classList.remove('hidden');
                designPreviewArea.classList.add('hidden');
                
                // Disable checkout button
                if (checkoutBtn) {
                    checkoutBtn.disabled = true;
                }
            });
        }
        
        // Design position controls
        function updateDesignPosition() {
            if (designPreview && designPath) {
                const x = positionX.value;
                const y = positionY.value;
                const scale = designScale.value;
                const rotation = designRotation.value;
                
                designPreview.style.left = x + '%';
                designPreview.style.top = y + '%';
                designPreview.style.transform = `translate(-50%, -50%) scale(${scale/100}) rotate(${rotation}deg)`;
            }
        }
        
        if (positionX && positionY && designScale && designRotation) {
            positionX.addEventListener('input', updateDesignPosition);
            positionY.addEventListener('input', updateDesignPosition);
            designScale.addEventListener('input', updateDesignPosition);
            designRotation.addEventListener('input', updateDesignPosition);
        }
        
        // Checkout button
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', function() {
                if (!designPath) {
                    alert('Please upload a design first');
                    return;
                }
                
                const color = document.querySelector('input[name="tshirtColor"]:checked').value;
                const size = sizeSelect.value;
                const quantity = parseInt(quantityInput.value);
                const x = positionX.value;
                const y = positionY.value;
                const scale = designScale.value;
                const rotation = designRotation.value;
                
                // Add to cart
                fetch('/api/add-to-cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        color: color,
                        size: size,
                        quantity: quantity,
                        designPath: designPath,
                        positionX: x,
                        positionY: y,
                        scale: scale,
                        rotation: rotation
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update cart count
                        const cartCountElements = document.querySelectorAll('.cart-count');
                        cartCountElements.forEach(function(element) {
                            element.textContent = data.cartCount;
                        });
                        
                        // Redirect to cart page
                        window.location.href = '/cart';
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
            });
        }
        
        // Initialize
        updateSummary();
    });
    """
    return app.response_class(js_code, mimetype='application/javascript')

@app.route('/api/cart-count')
def api_cart_count():
    cart = session.get('cart', [])
    return jsonify({'count': len(cart)})

# Main entry point
if __name__ == '__main__':
    # Move HTML files to templates directory
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Create placeholder images for t-shirts
    for color in ['black', 'white', 'gray']:
        with open(f'static/img/tshirt-{color}.png', 'w') as f:
            f.write(f'Placeholder for {color} t-shirt image')
    
    # Create placeholder images for designs
    for i in range(1, 7):
        with open(f'static/img/design{i}.jpg', 'w') as f:
            f.write(f'Placeholder for design {i} image')
    
    # Create placeholder images for avatars
    for i in range(1, 4):
        with open(f'static/img/avatar{i}.jpg', 'w') as f:
            f.write(f'Placeholder for avatar {i} image')
    
    # Create placeholder images for team members
    for i in range(1, 5):
        with open(f'static/img/team{i}.jpg', 'w') as f:
            f.write(f'Placeholder for team {i} image')
    
    print("Server is running at http://127.0.0.1:5000/")
    app.run(debug=True)