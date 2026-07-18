# 🔐 Secure Password Manager

A command-line password manager built with Python that securely stores encrypted passwords using Fernet encryption.

## Features

- Master Password Authentication
- Password Encryption (Fernet)
- PBKDF2 Key Derivation
- Password Generator
- Password Strength Checker
- Store Passwords
- Search Passwords
- Edit Passwords
- Delete Passwords
- JSON Storage
- Creation & Last Modified Date
- Username & Website Validation
- Auto Lock
- Wrong Password Attempt Limit
- Colored Terminal Interface
- Logging

## Technologies Used

- Python
- Cryptography
- Colorama
- JSON
- Logging

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python password_manager.py
```

## Security

Passwords are encrypted before storage.
The master password is never stored directly.
PBKDF2 with SHA-256 is used for key derivation.

## Author

Aryan