# 🔐 Password Manager (Python)

A secure command-line Password Manager built with Python.

Passwords are encrypted using AES encryption provided by the Cryptography (Fernet) library and protected with a Master Password.

---

## Features

- Master Password Authentication
- AES Encryption (Fernet)
- Secure Password Storage
- Password Generator
- Password Strength Checker
- Search Passwords
- Edit Passwords
- Delete Passwords
- Auto Lock after inactivity
- Logging System
- Duplicate Website Detection
- Website Validation
- Username Validation
- Creation & Modification Date Tracking
- Colored Console Output

---

## Technologies Used

- Python 3
- Cryptography
- Colorama
- JSON
- Logging
- Regular Expressions

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/password-manager.git
```

Move inside project

```bash
cd password-manager
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python password_manager.py
```

---

## Project Structure

```
Password-Manager
│
├── password_manager.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── passwords.json
└── assets
```

---

## Security

Passwords are never stored in plain text.

The project uses

- PBKDF2-HMAC-SHA256
- 480,000 iterations
- Fernet Encryption (AES)
- Random Salt
- Master Password Authentication

---

## Future Improvements

- GUI Version
- Cloud Backup
- Password Categories
- Password Expiry Notifications
- Export/Import Passwords
- Two-Factor Authentication
- Dark Mode GUI

---

## Author

Aryan Upadhyay
