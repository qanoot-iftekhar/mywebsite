"""
Fix corrupted base.html by properly separating head and body sections
"""

# Read the corrupted file
with open('main/templates/base.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find where announcement-bar incorrectly starts in head
corrupted_start = None
for i, line in enumerate(lines):
    if '<div class="announcement-bar">' in line and i < 50:  # Should be in head if corrupted
        corrupted_start = i
        break

if corrupted_start:
    print(f"Found corruption at line {corrupted_start + 1}")
    
    # Split into head and body parts
    head_part = lines[:13]  # Up to fonts link
    
    # Add missing head closing tags
    head_part.extend([
        '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n',
        '    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">\n',
        '\n',
        '    <!-- Font Awesome -->\n',
        '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n',
        '\n',
        '    <!-- CSS -->\n',
        '    <link rel="stylesheet" href="{% static \'css/style.css\' %}">\n',
        '    <link rel="stylesheet" href="{% static \'css/navbar.css\' %}">\n',
        '    <link rel="stylesheet" href="{% static \'css/animations.css\' %}">\n',
        '    {% block extra_css %}{% endblock %}\n',
        '</head>\n',
        '\n',
        '<body>\n',
    ])
    
    # Body part starts from announcement-bar
    body_part = lines[corrupted_start:]
    
    # Combine
    fixed_lines = head_part + body_part
    
    # Write back
    with open('main/templates/base.html', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("File structure fixed!")
    print("- Head tag properly closed")
    print("- Body tag added")
    print("- CSS files included")
else:
    print("No corruption found or already fixed")
