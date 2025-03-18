import os
import re

def convert_html_to_template(html_content):
    # Replace hardcoded year with template variable
    html_content = re.sub(r'<span id="currentYear">[^<]*</span>', 
                          '<span id="currentYear">{{ current_year }}</span>', 
                          html_content)
    
    # Replace email protection with actual email
    html_content = re.sub(r'<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="[^"]*">\[email&#160;protected\]</a>', 
                          'info@customsatg.com', 
                          html_content)
    
    # Remove Cloudflare email protection script
    html_content = re.sub(r'<script data-cfasync="false" src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"></script>', 
                          '', 
                          html_content)
    
    # Update CSS and JS paths
    html_content = html_content.replace('href="css/', 'href="{{ url_for(\'static\', filename=\'css/')}}\"')
    html_content = html_content.replace('src="js/', 'src="{{ url_for(\'static\', filename=\'js/')}}\"')
    html_content = html_content.replace('src="img/', 'src="{{ url_for(\'static\', filename=\'img/')}}\"')
    
    return html_content

def process_html_files():
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # HTML files to process
    html_files = {
        'index.html': 'index.html',
        'customize.html': 'customize.html',
        'about.html': 'about.html',
        'contact.html': 'contact.html',
        'login.html': 'login.html'
    }
    
    for source_file, target_file in html_files.items():
        if os.path.exists(source_file):
            with open(source_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Convert HTML to template
            template_content = convert_html_to_template(html_content)
            
            # Write to templates directory
            with open(os.path.join('templates', target_file), 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            print(f"Converted {source_file} to template {target_file}")
        else:
            print(f"Warning: {source_file} not found")

def process_css_file():
    # Create static/css directory if it doesn't exist
    os.makedirs('static/css', exist_ok=True)
    
    if os.path.exists('styles.css'):
        with open('styles.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Write to static/css directory
        with open(os.path.join('static/css', 'styles.css'), 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print("Copied styles.css to static/css/styles.css")
    else:
        print("Warning: styles.css not found")

if __name__ == '__main__':
    process_html_files()
    process_css_file()
    print("Conversion complete!")