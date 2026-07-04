@"
# 🔐 Password Manager

A secure CLI password manager with AES-GCM encryption and Argon2id hashing.

## Features
- Master password authentication with Argon2id
- AES-GCM encryption for stored passwords
- Generate strong passwords
- CLI interface

## Installation
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage
\`\`\`bash
# Setup vault
python pm.py setup

# Add a password
python pm.py add github username password123

# Generate a strong password
python pm.py generate twitter username 20

# List all entries
python pm.py list

# Retrieve a password
python pm.py get github
\`\`\`
"@ | Out-File -FilePath README.md -Encoding utf8