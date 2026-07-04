@"
# 🔐 Password Manager

A secure CLI password manager with AES-GCM encryption and Argon2id hashing.

## Features

- 🔒 **Master password** authentication with Argon2id (memory-hard hashing)
- 🛡️ **AES-GCM** encryption for all stored passwords
- 🔑 **PBKDF2** key derivation with salt
- 🎲 **Cryptographically secure** password generation
- 💻 **Simple CLI** interface

## Installation


# Clone the repository
```bash
git clone https://github.com/yazuu07/password-manager.git
cd password-manager
```

# Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

```bash
# Initialize vault
python pm.py setup
```

# Add a password
```bash
python pm.py add github username password123
```

# Generate a strong password
```bash
python pm.py generate gmail username 20
```

# List all entries
```bash
python pm.py list
```

# Retrieve a password
```bash
python pm.py get github
```

# Delete an entry
```bash
python pm.py delete github
```

## Security Architecture

```
Master Password (User Input)
        ↓
Argon2id Hash (stored for authentication)
        ↓
PBKDF2 + Salt → AES-256 Key
        ↓
AES-GCM Encryption (vault.json encrypted)
```

## Security Notes

- ⚠️ This is for educational purposes
- 🔐 Never share your \`data/\` directory
- 🗝️ No password recovery - backup your master password
