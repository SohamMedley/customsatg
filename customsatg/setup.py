import os
import sys
import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"Successfully ran {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        sys.exit(1)

def main():
    print("Setting up CustomsATG Website...")
    
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    
    # Run setup scripts
    run_script('convert_html_to_templates.py')
    run_script('generate_cart_page.py')
    run_script('generate_cart_js.py')
    
    # Add API endpoints to app.py
    print("Adding cart API endpoints to app.py...")
    with open('app.py', 'r') as f:
        app_py = f.read()
    
    # Check if endpoints already exist
    if '@app.route(\'/api/update-cart-item\'' not in app_py:
        # Add update-cart-item endpoint
        update_endpoint = """
@app.route('/api/update-cart-item', methods=['POST'])
def api_update_cart_item():
    data = request.json
    item_id = data.get('id')
    quantity = data.get('quantity', 1)
    
    # Get cart from session
    cart = session.get('cart', [])
    
    # Find and update item
    for item in cart:
        if item['id'] == item_id:
            item['quantity'] = quantity
            item['totalPrice'] = (item['price'] + item['printPrice']) * quantity
            break
    
    # Update cart in session
    session['cart'] = cart
    
    return jsonify({
        'success': True, 
        'message': 'Cart updated'
    })
"""
        # Add remove-cart-item endpoint
        remove_endpoint = """
@app.route('/api/remove-cart-item', methods=['POST'])
def api_remove_cart_item():
    data = request.json
    item_id = data.get('id')
    
    # Get cart from session
    cart = session.get('cart', [])
    
    # Remove item
    cart = [item for item in cart if item['id'] != item_id]
    
    # Update cart in session
    session['cart'] = cart
    
    return jsonify({
        'success': True, 
        'message': 'Item removed from cart'
    })
"""
        # Insert endpoints before the main entry point
        app_py = app_py.replace("# Main entry point", update_endpoint + remove_endpoint + "\n# Main entry point")
        
        with open('app.py', 'w') as f:
            f.write(app_py)
    
    print("Setup complete! Run the application with 'python app.py'")

if __name__ == '__main__':
    main()