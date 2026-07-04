@"
#!/usr/bin/env python3
import sys
import getpass
import os
import json
from vault import Vault
from crypto import hash_master_password, verify_master_password

VAULT_FILE = "data/vault.json"
HASH_FILE = "data/master.hash"

def setup():
    if os.path.exists(VAULT_FILE):
        print("⚠️  Vault already exists.")
        return
    
    print("\n🔐 Welcome to Password Manager!")
    print("Let's set up your master password.\n")
    
    while True:
        password = getpass.getpass("Set master password: ")
        confirm = getpass.getpass("Confirm master password: ")
        if password == confirm and len(password) >= 8:
            break
        elif len(password) < 8:
            print("❌ Password must be at least 8 characters.")
        else:
            print("❌ Passwords do not match.")
    
    os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)
    with open(VAULT_FILE, 'w') as f:
        json.dump({'ciphertext': '', 'nonce': '', 'salt': ''}, f)
    
    with open(HASH_FILE, 'w') as f:
        f.write(hash_master_password(password))
    
    print("✅ Vault created successfully!")

def unlock() -> Vault:
    if not os.path.exists(HASH_FILE):
        print("❌ No vault found. Run 'python pm.py setup' first.")
        sys.exit(1)
    
    with open(HASH_FILE, 'r') as f:
        stored_hash = f.read().strip()
    
    attempts = 3
    while attempts > 0:
        password = getpass.getpass("Enter master password: ")
        if verify_master_password(password, stored_hash):
            return Vault(password)
        attempts -= 1
        print(f"❌ Wrong password. {attempts} attempts remaining.")
    
    print("🔒 Too many failed attempts. Exiting.")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("""
🔐 Password Manager CLI

Commands:
  setup                    Initialize a new vault
  add <service> <username> [password]  Add a password
  get <service>            Retrieve a password
  list                     List all services
  delete <service>         Delete a service
  generate <service> <username> [length]  Generate and store a password
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        setup()
        return
    
    vault = unlock()
    
    if command == "add":
        if len(sys.argv) < 4:
            print("Usage: pm add <service> <username> [password]")
            return
        service, username = sys.argv[2], sys.argv[3]
        password = sys.argv[4] if len(sys.argv) > 4 else None
        if password:
            vault.add_entry(service, username, password)
        else:
            vault.generate_and_add(service, username)
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: pm get <service>")
            return
        vault.get_entry(sys.argv[2])
    
    elif command == "list":
        vault.list_entries()
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: pm delete <service>")
            return
        vault.delete_entry(sys.argv[2])
    
    elif command == "generate":
        if len(sys.argv) < 4:
            print("Usage: pm generate <service> <username> [length]")
            return
        service, username = sys.argv[2], sys.argv[3]
        length = int(sys.argv[4]) if len(sys.argv) > 4 else 16
        vault.generate_and_add(service, username, length)
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
"@ | Out-File -FilePath pm.py -Encoding utf8