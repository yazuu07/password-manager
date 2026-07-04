@"
import json
import os
from typing import Dict, Optional
from datetime import datetime
from crypto import encrypt_data, decrypt_data, generate_password

VAULT_FILE = "data/vault.json"

class Vault:
    def __init__(self, master_password: str):
        self.master_password = master_password
        self.entries = {}
        self._load()
    
    def _load(self):
        if not os.path.exists(VAULT_FILE):
            self.entries = {}
            return
        
        try:
            with open(VAULT_FILE, 'r') as f:
                encrypted_vault = json.load(f)
            
            if encrypted_vault and encrypted_vault.get('ciphertext'):
                decrypted_json = decrypt_data(
                    encrypted_vault['ciphertext'],
                    encrypted_vault['nonce'],
                    encrypted_vault['salt'],
                    self.master_password
                )
                self.entries = json.loads(decrypted_json)
            else:
                self.entries = {}
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️  Vault error: {e}")
            self.entries = {}
    
    def _save(self):
        os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)
        
        json_data = json.dumps(self.entries)
        ciphertext, nonce, salt = encrypt_data(json_data, self.master_password)
        
        with open(VAULT_FILE, 'w') as f:
            json.dump({
                'ciphertext': ciphertext,
                'nonce': nonce,
                'salt': salt
            }, f)
        print("✅ Vault saved.")
    
    def add_entry(self, service: str, username: str, password: str):
        if service in self.entries:
            overwrite = input(f"⚠️  Service '{service}' exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                return
        
        self.entries[service] = {
            'username': username,
            'password': password,
            'created': str(datetime.now())
        }
        self._save()
        print(f"✅ Password for '{service}' added!")
    
    def get_entry(self, service: str) -> Optional[Dict]:
        if service not in self.entries:
            print(f"❌ Service '{service}' not found.")
            return None
        
        entry = self.entries[service]
        print(f"\n🔑 Service: {service}")
        print(f"   Username: {entry['username']}")
        print(f"   Password: {entry['password']}")
        print(f"   Created: {entry.get('created', 'Unknown')}")
        return entry
    
    def list_entries(self):
        if not self.entries:
            print("📭 Vault is empty.")
            return
        
        print("\n📋 Stored Services:")
        print("-" * 40)
        for service, entry in sorted(self.entries.items()):
            print(f"  • {service} (user: {entry['username']})")
        print("-" * 40)
        print(f"Total: {len(self.entries)} entries")
    
    def delete_entry(self, service: str):
        if service not in self.entries:
            print(f"❌ Service '{service}' not found.")
            return
        
        confirm = input(f"⚠️  Delete '{service}'? (y/n): ").lower()
        if confirm == 'y':
            del self.entries[service]
            self._save()
            print(f"✅ '{service}' deleted.")
    
    def generate_and_add(self, service: str, username: str, length: int = 16):
        password = generate_password(length)
        self.add_entry(service, username, password)
        print(f"🔐 Generated password: {password}")
"@ | Out-File -FilePath vault.py -Encoding utf8