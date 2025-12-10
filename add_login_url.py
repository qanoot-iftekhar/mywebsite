import sys

# Read the settings file
with open('mywebsite/settings.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with DEFAULT_AUTO_FIELD
insert_index = None
for i, line in enumerate(lines):
    if "DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'" in line:
        insert_index = i + 1
        break

if insert_index is None:
    print("Could not find DEFAULT_AUTO_FIELD line")
    sys.exit(1)

# Insert the new lines
new_lines = [
    '\n',
    '# Login/Logout URLs - Fix for @login_required redirect\n',
    "LOGIN_URL = 'login'  # Redirect to /login/ instead of /accounts/login/\n",
    "LOGIN_REDIRECT_URL = 'home'  # After successful login\n",
    "LOGOUT_REDIRECT_URL = 'home'  # After logout\n"
]

lines = lines[:insert_index] + new_lines + lines[insert_index:]

# Write back
with open('mywebsite/settings.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("LOGIN_URL settings added successfully!")
