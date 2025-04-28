import json
import re
import random
import string

# Caesar cipher encryption and decryption functions (pre-implemented)
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# Password strength checker function (optional)
"""
    Rules to generate password:
    - At least 8 characters long
    - Contains uppercase and lowercase letters
    - Contains at least one digit
    - Contains at least one special character
"""
def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[^A-Za-z0-9]', password):
        return False
    return True


# Password generator function (optional)
def generate_password(length):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation
    
    characters = letters + digits + special
    print(characters)
    password = ""
    while len(password) < length:
        new_char = random.choice(characters)
        password += new_char

    if is_strong_password(password):
        return password
    else:
        return generate_password(length)
    

# Initialize empty lists to store encrypted passwords, websites, and usernames
encrypted_passwords = []
websites = []
usernames = []
SHIFT = 10  # Shift value to encrypt and decrypt using caesar cipher
DELIMITER = '¤' # divides the entries in vault.txt(never appears in string.punctuation)


# Function to add a new password 
def add_password():
    """
    Add a new password to the password manager.

    This function should prompt the user for the website, username,  and password and store them to lits with same index. Optionally, it should check password strengh with the function is_strong_password. It may also include an option for the user to
    generate a random strong password by calling the generate_password function.
    Returns:
        None
    """

    website = input("Enter website: ").strip()
    username = input("Enter username: ").strip()
    
    while True:
        choice = input("Generate password? (y/n): ").lower()
        if choice == 'y':
            length = int(input("Enter password length (default 8): ") or 8)
            password = generate_password(length)
            print(f"Generated password: {password}")
            break
        elif choice == 'n':
            password = input("Enter password: ")
            if not is_strong_password(password):
                print("Warning: Password is not strong!")
                continue_anyway = input("Continue anyway? (y/n): ").lower()
                if continue_anyway != 'y':
                    continue
            break
        else:
            print("Invalid choice")
    
    encrypted_passwords.append(caesar_encrypt(password, SHIFT))
    websites.append(website)
    usernames.append(username)
    print("Password added successfully!")

# Function to retrieve a password 
def get_password():
    """
    Retrieve a password for a given website.
    This function should prompt the user for the website name and
    then display the username and decrypted password for that website.
    Returns:
        None
    """
    website = input("Enter website: ").strip()
    try:
        index = websites.index(website)
        decrypted = caesar_decrypt(encrypted_passwords[index], SHIFT)
        print(f"\nWebsite: {website}")
        print(f"Username: {usernames[index]}")
        print(f"Password: {decrypted}\n")
    except ValueError:
        print("Website not found in vault")



# Function to save passwords to a JSON file 
def save_passwords():
 
    """
    Save the password vault to a file.
    This function should save passwords, websites, and usernames to a text
    file named "vault.txt" in a structured format.
    Returns:
        None
    """
    try:
      with open('vault.txt', 'w') as f:
        # write the headers
        f.write(f"{'SerialNo'} {DELIMITER} {'Website'} {DELIMITER} {'Username'} {DELIMITER} {'Password'}\n")
        for i in range(len(websites)):
            f.write(f"#{i+1}: {websites[i]} {DELIMITER} {usernames[i]} {DELIMITER} {encrypted_passwords[i]}\n") 
            #starts with "#{i}" to check while loading
      print("Passwords saved to vault.txt with numbered entries")
    except Exception as e:
      print(f"Error saving passwords: {str(e)}")

# Function to load passwords from a JSON file 
def load_passwords():
    """
    Load passwords from a file into the password vault.
    This function should load passwords, websites, and usernames from a text
    file named "vault.txt" (or a more generic name) and populate the respective lists.
    Returns:
       None
       -- I changed it to return True or False so that i can use it to deliver success or failure message.
    """
    # clear the lists before loading (avoids duplicates)
    websites.clear()
    usernames.clear()
    encrypted_passwords.clear()

    try:
        with open("vault.txt", "r") as file:
            for line in file:
                if line.startswith("#"): 
                    parts = line.split(DELIMITER)
                    if len(parts) == 3:
                        websites.append(parts[0].split(':')[1].strip())
                        usernames.append(parts[1].strip())
                        encrypted_passwords.append(parts[2].strip())
        print(websites, usernames, encrypted_passwords)               
        return True
    except FileNotFoundError:
        print("Error: vault.txt not found")
        return False
    except Exception as e:
        print(f"Error loading passwords: {str(e)}")
        return False      
      

# Main method
def main():
  
  while True:
    print("\nPassword Manager Menu:")
    print("1. Add Password")
    print("2. Get Password")
    print("3. Save Passwords")
    print("4. Load Passwords")
    print("5. Quit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_password()
    elif choice == "2":
        get_password()
    elif choice == "3":
        save_passwords()
    elif choice == "4":
        passwords = load_passwords()
        # minor changes: Utilizing the boolean return value of the function to print the result.
        if passwords == True:
            print("Passwords alongside websites and usernames loaded successfully!", passwords)
        else:
            print("Problem loading passwords, websites and usernames!", passwords)
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")


# Execute the main function when the program is run
if __name__ == "__main__":
    main()
