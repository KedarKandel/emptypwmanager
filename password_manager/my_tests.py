import unittest
import os
import string
from main import (
    generate_password,
    save_passwords,
    load_passwords,
    is_strong_password,
    websites, usernames, encrypted_passwords,
    DELIMITER
)

class TestPasswordManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize test data"""
        cls.test_websites = ["www.google.com", "github.com"]
        cls.test_usernames = ["www.testuser1", "dev2023"]
        cls.test_passwords = ["T€stP@ss1", "S3cur3Pwd§"]
        cls.test_file = "test_vault.txt"

    def setUp(self):
        """Reset global variables before each test"""
        websites.clear()
        usernames.clear()
        encrypted_passwords.clear()
        self._remove_test_file()

    def _remove_test_file(self):
        """clean file state"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)    

    def test_generate_password(self):
        # Test length
        pwd = generate_password(12)
        self.assertEqual(len(pwd), 12)
        
        # Test if different character exists in the password
        pwd = generate_password(12)
        self.assertTrue(any(c in string.ascii_letters for c in pwd))
        self.assertTrue(any(c in string.digits for c in pwd))
        self.assertTrue(any(c in string.punctuation for c in pwd))

    def test_password_strength(self):
        self.assertTrue(is_strong_password("S3cur3P@ss!"))
        self.assertFalse(is_strong_password("weak"))
        self.assertFalse(is_strong_password("noSpecialChars123"))

    def test_save_and_load(self):
        """Test saving and loading with consistent filenames"""
       
        # Prepare test data
        websites.extend(self.test_websites)
        usernames.extend(self.test_usernames)
        encrypted_passwords.extend(self.test_passwords)
        
        # Test saving
        save_passwords(filename="test_vault.txt")
        self.assertTrue(os.path.exists(self.test_file))
        
        # Verify file content
        with open(self.test_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            self.assertIn(DELIMITER, first_line)
        
        # Test loading
        websites.clear()
        usernames.clear()
        encrypted_passwords.clear()
        
        load_passwords(filename="test_vault.txt")
        self.assertEqual(len(websites), 2)
        self.assertEqual(websites[0], self.test_websites[0])
        self.assertEqual(usernames[1], self.test_usernames[1])
      

    def test_delimiter_safety(self):
        ''' Verify delimiter isn't in any character set'''
        self.assertNotIn(DELIMITER, string.ascii_letters)
        self.assertNotIn(DELIMITER, string.digits)
        self.assertNotIn(DELIMITER, string.punctuation)

    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()