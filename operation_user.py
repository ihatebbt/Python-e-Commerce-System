from model_admin import Admin
from model_customer import Customer
from io_interface import IOInterface
import random
import string
import re


class UserOperation:
    io = IOInterface()
#This method generates a unique user ID by concatenating the prefix "u_" with a random string of 10 digits.
    def generate_unique_user_id(self):
        unique_id = "u_" + ''.join(random.choices(string.digits, k=10))
        return unique_id
#This method encrypts the user password using a simple encryption algorithm. It generates a random string of letters and digits, 
#and then combines it with the original password by interleaving the characters. The resulting encrypted password is wrapped with 
#special characters "^^" and "$$" for identification.
    def encrypt_password(self, user_password):
        random_string = ''.join(random.choices(
            string.ascii_letters + string.digits, k=len(user_password) * 2))
        encrypted_password = ""
        for i in range(len(user_password)):
            encrypted_password += random_string[i*2:i*2+2] + user_password[i]
        encrypted_password = "^^" + encrypted_password + "$$"
        return encrypted_password
#This method decrypts the encrypted password by extracting the original password from the encrypted string. It removes the special 
#characters and retrieves the original password by selecting every third character starting from the 4th index.
    def decrypt_password(self, encrypted_password):
        #As we have ^^ at the start of password and then we have 2 random letters/numbers so our password starts from 5 element or 4th index
        decrypted_password = encrypted_password[4:-2:3]
        return decrypted_password
#This method checks if a username already exists in the user data file. It reads the user data from the file, extracts the usernames, and checks 
#if the given username matches any of the existing usernames. It returns True if the username exists, and False otherwise.
    def check_username_exist(self, user_name):
        with open("data/users.txt", "r", encoding="utf-8") as file:
            #Read all lines in the file
            user_data = file.readlines()
            #Split the string on comma
            dict_user_names = [line.split(",")[1] for line in user_data]

            user_names = [line.split(':')[1].strip().strip("''") for line in dict_user_names]
            # if user_name in user_names:
            #     return True
            # else:
            #     return False
            return user_name in user_names
#This method validates a username by checking its length and composition. It ensures that the username is at least 5 characters long and consists of alphabetic 
#characters and underscores only. It returns True if the username is valid, and False otherwise.
    def validate_username(self, user_name):

        return len(user_name) >= 5 and all(char.isalpha() or char == '_' for char in user_name)

    def validate_password(self, user_password):

        return len(user_password) >= 5 and any(char.isalpha() for char in user_password) and any(char.isdigit() for char in user_password)
#This method handles the login process for a user. It reads the user data from the file and compares the provided username and password with the stored values. 
#If a match is found, it determines the user's role (admin or customer) and creates an object of the corresponding class (Admin or Customer) with the extracted 
#user data. If no match is found, an error message is displayed, and None is returned.
    def login(self, user_name, user_password):
        with open("data/users.txt", "r", encoding="utf-8") as file:
            user_data = file.readlines()
            for line in user_data:
                #Extract values within '....' using regular expression
                pattern = r": ('.*?')[,}]"
                values = re.findall(pattern, line)

                #Remove the values corresponding to dictionary keys
                all_data = [value.strip("'") for value in values]
                line_user_name = all_data[1]
                line_user_password = self.decrypt_password(all_data[2])
                if line_user_name == user_name and line_user_password == user_password:
                    role = all_data[4]
                    all_data[2] = line_user_password
                    if role == "customer":
                        #Create and return a Customer object
                        return Customer(*all_data)
                    elif role == "admin":
                        #Create and return an Admin object
                        return Admin(*all_data)
        self.io.print_error_message("UserOperation.login",
                               "username or password incorrect")
        return None