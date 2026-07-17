# 🔐 Password Manager (Python)

A secure terminal-based password manager built with Python.

## Features

- Master Password Authentication
- Password Encryption using Fernet
- PBKDF2 Key Derivation
- Store Passwords Securely
- View Passwords
- Search Passwords
- Edit Passwords
- Delete Passwords
- JSON Storage
- Creation & Last Modified Dates
- Username & Website Validation
- Colored Terminal Interface
- Wrong Password Attempt Protection
- Auto Lock

## Technologies Used

- Python
- Cryptography
- Colorama
- JSON

## Installation

```bash
pip install cryptography colorama
```

## Run

```bash
python main.py
```

## Security

- Passwords are encrypted using Fernet.
- Master password is converted into an encryption key using PBKDF2.
- The master password itself is never stored.

## Screenshots

(Add screenshots here later.)
