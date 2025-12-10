import sys

# Read the settings file
with open('mywebsite/settings.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove duplicate LOGIN_URL block (lines 126-129)
# Keep only the first occurrence (lines 121-124)
new_lines = []
skip_next_login_block = False
login_block_count = 0

for i, line in enumerate(lines):
    if '# Login/Logout URLs - Fix for @login_required redirect' in line:
        login_block_count += 1
        if login_block_count == 1:
            # Keep the first block
            new_lines.append(line)
        else:
            # Skip the second block (and next 4 lines)
            skip_next_login_block = True
            continue
    elif skip_next_login_block and login_block_count == 2:
        # Skip the duplicate lines
        if 'LOGIN_URL' in line or 'LOGIN_REDIRECT_URL' in line or 'LOGOUT_REDIRECT_URL' in line or (line.strip() == '' and i < len(lines)-1 and '# REST Framework' in lines[i+1]):
            continue
        else:
            skip_next_login_block = False
            new_lines.append(line)
    else:
        new_lines.append(line)

# Write back
with open('mywebsite/settings.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Duplicate LOGIN_URL settings removed successfully!")
