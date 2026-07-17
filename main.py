import os
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import re
import json
import logging
from datetime import datetime
import time

from colorama import Fore, Style, init

init(autoreset=True)    

SUCCESS = Fore.GREEN
ERROR = Fore.RED
WARNING = Fore.YELLOW
INFO = Fore.CYAN
TITLE = Fore.MAGENTA
RESET = Style.RESET_ALL

VERIFICATION_FILE = "verify.key"
VERIFICATION_TEXT = "PASSWORD_MANAGER_VERIFIED"
MAX_ATTEMPTS = 5
AUTO_LOCK_TIME = 180   

PASSWORD_FILE = "passwords.json"
SALT_FILE = "salt.key"
LOG_FILE = "password_manager.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        return []
    try:
        with open(PASSWORD_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_passwords(data):
    with open(PASSWORD_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_salt():
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()

    return salt

def generate_key(master_password):
    salt = load_salt()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(master_password.encode())
    )

    return Fernet(key)  


def setup_master_password():
    if not os.path.exists(VERIFICATION_FILE):
        print("\nNo master password found.")
        print("Let's create one.\n")

        while True:
            password1 = input(INFO + "Create Master Password: " + RESET).strip()
            password2 = input(INFO + "Confirm Master Password: " + RESET).strip()

            if not password1:
                print(ERROR + "Master password cannot be empty.\n")
                continue

            if password1 != password2:
                print(ERROR + "Passwords do not match.\n")
                continue

            fer = generate_key(password1)

            with open(VERIFICATION_FILE, "w") as f:
                f.write(
                    fer.encrypt(VERIFICATION_TEXT.encode()).decode()
                )

            logging.info("Master password created.")
            print(SUCCESS + "\nMaster password created successfully!\n")
            return fer    


    else:
        attempts = MAX_ATTEMPTS

        while attempts > 0:
            password = input(WARNING + "Enter Master Password: " + RESET).strip()

            fer = generate_key(password)

            with open(VERIFICATION_FILE, "r") as f:
                encrypted = f.read()

            try:
                text = fer.decrypt(encrypted.encode()).decode()

                if text == VERIFICATION_TEXT:
                    logging.info("Master password verified.")
                    print("\nAccess Granted!\n")
                    return fer

            except InvalidToken:
                attempts -= 1

                if attempts == 0:
                    print(ERROR + "\nToo many incorrect attempts.")
                    exit()
                logging.warning("Failed master password attempt. %d attempt(s) left.", attempts)
                print(ERROR + f"\nWrong Password! Attempts Left: {attempts}\n")

fer = setup_master_password()                
def add():

    while True:
        website = input(INFO + "Website: " + RESET).strip()

        if validate_website(website):
            break

    while True:
        username = input(INFO + "Username: " + RESET).strip()

        if validate_username(username):
            break

    while True:
        password = input(INFO + "Password: " + RESET).strip()

        if password:
            break

        print(ERROR + "Password cannot be empty." + RESET)



    passwords = load_passwords()

    for account in passwords:
        if account["website"].lower() == website.lower():
            print(ERROR + "\nWebsite already exists.\n" + RESET)
            return

    encrypted = fer.encrypt(password.encode()).decode()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    passwords.append({
        "website": website,
        "username": username,
        "password": encrypted,
        "created": current_time,
        "modified": current_time
    })

    save_passwords(passwords)

    print(SUCCESS + "\nPassword stored successfully!\n" + RESET)
def view():

    passwords = load_passwords()

    if not passwords:
        print(WARNING + "\nNo passwords stored.\n" + RESET)
        return
    
    logging.info("Viewed all stored passwords.")

    for account in passwords:

        decrypted = fer.decrypt(
            account["password"].encode()
        ).decode()
 
        logging.info("Searched and revealed entry for website '%s'.", account["website"])

        print(INFO + "-" * 45 + RESET)
        print(f"Website       : {account['website']}")
        print(f"Username      : {account['username']}")
        print(f"Password      : {decrypted}")
        print(f"Created On    : {account['created']}")
        print(f"Last Modified : {account['modified']}")

    
    
def search():

    website = input(INFO + "Search Website: " + RESET).strip().lower()

    passwords = load_passwords()

    for account in passwords:

        if account["website"].lower() == website:

            decrypted = fer.decrypt(
                account["password"].encode()
            ).decode()

            print(INFO + "-" * 45 + RESET)
            print(f"Website       : {account['website']}")
            print(f"Username      : {account['username']}")
            print(f"Password      : {decrypted}")
            print(f"Created On    : {account['created']}")
            print(f"Last Modified : {account['modified']}")
            return

    print(ERROR + "\nWebsite not found.\n" + RESET)
def delete():

    website = input(INFO + "Website to delete: " + RESET).strip().lower()

    passwords = load_passwords()

    new_list = []

    deleted = False

    for account in passwords:

        if account["website"].lower() == website:
            deleted = True
            continue

        new_list.append(account)

    save_passwords(new_list)

    if deleted:
        logging.info("Deleted entry for website '%s'.", website)
        print(SUCCESS + "\nPassword deleted.\n" + RESET)
    else:
        print(ERROR + "\nWebsite not found.\n" + RESET)

def edit():

    website = input(INFO + "Website to edit: " + RESET).strip().lower()

    passwords = load_passwords()

    for account in passwords:

        if account["website"].lower() == website:

            new_username = input("New Username: ").strip()

            new_password = input("New Password: ").strip()

            if new_username:
                account["username"] = new_username

            if new_password:
                account["password"] = fer.encrypt(
                    new_password.encode()
                ).decode()

            account["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            save_passwords(passwords)
            logging.info("Edited entry for website '%s'.", account["website"])
            print(SUCCESS + "\nPassword Updated Successfully.\n" + RESET)
            return

    print(ERROR + "\nWebsite not found.\n" + RESET)

def validate_website(website):

    if website == "":
        print(ERROR + "\n✖ Website cannot be empty.\n" + RESET)
        return False

    pattern = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"

    if re.match(pattern, website):
        return True

    print(ERROR + "\n✖ Invalid website name." + RESET)
    print(INFO + "Examples: google.com, github.com, amazon.in, chat.openai.com\n" + RESET)
    return False


def validate_username(username):

    if username == "":
        print(ERROR + "\n✖ Username cannot be empty.\n" + RESET)
        return False

    pattern = r"^[A-Za-z0-9.-]{2,100}$"

    if re.match(pattern, username):
        return True

    print(ERROR + "\n✖ Invalid username." + RESET)
    print(INFO + "Username can contain:" + RESET)
    print(WARNING + "• Letters (A-Z, a-z)")
    print("• Numbers (0-9)")
    print("• @ . _ + -")
    print("• Length: 3-50 characters\n" + RESET)

    return False        

last_activity = time.time()

while True:

    if time.time() - last_activity >= AUTO_LOCK_TIME:

     print(ERROR + "\nSession Locked!\n")

    password = input(WARNING + "Enter Master Password: " + RESET)

    try:

        temp = generate_key(password)

        with open("verify.key", "r") as f:
                encrypted = f.read()

        temp.decrypt(encrypted.encode())

        fer = temp

        print(SUCCESS + "\nUnlocked Successfully!\n")

        break  

    except InvalidToken:
        print(ERROR + "Wrong Password.")


while True:

    last_activity = time.time()

    print(TITLE + "=" * 50)
    print(WARNING + "       WELCOME TO PASSWORD MANAGER")
    print(TITLE + "=" * 50 + RESET)

    print(INFO + "1." + RESET + " Store New Password")
    print(INFO + "2." + RESET + " View All Passwords")
    print(INFO + "3." + RESET + " Search by Website")
    print(INFO + "4." + RESET + " Edit Password")
    print(INFO + "5." + RESET + " Delete Password")
    print(ERROR + "Q." + RESET + " Quit")

    print(TITLE + "=" * 50 + RESET)

    choice = input("\nChoose an option: ").lower().strip()

    if choice == "1":
        add()
        last_activity = time.time()

    elif choice == "2":
        view()
        last_activity = time.time()

    elif choice == "3":
        search()
        last_activity = time.time()

    elif choice == "4":
        edit()
        last_activity = time.time()

    elif choice == "5":
        delete()
        last_activity = time.time()

    elif choice == "q":
        print(WARNING + "\nExiting Password Manager...")
        logging.info("Application closed by user.")
        print(SUCCESS + "Goodbye!")
        break

    else:
        print(ERROR + "Invalid option.")