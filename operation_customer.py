from io_interface import IOInterface
from operation_user import UserOperation
from model_customer import Customer

import re
import time


class CustomerOperation:
    io = IOInterface()
    # class variable to work with UserOperation methods
    user_operation = UserOperation()
#Validates the format of an email address using a regular expression pattern.
    def validate_email(self, user_email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, user_email) is not None

    def validate_mobile(self, user_mobile):
        return re.match(r"^(04|03)\d{8}$", user_mobile) is not None
#Registers a new customer by creating a Customer object and saving it to a file. Validates the provided email and mobile number before registration.
    def register_customer(self, user_name, user_password, user_email, user_mobile):
        if not self.user_operation.validate_username(user_name):
            self.io.print_error_message(
                "CustomerOperation.register_customer", f"invalid username.")
            return False
        if not self.user_operation.validate_password(user_password):
            self.io.print_error_message(
                "CustomerOperation.register_customer", "invalid password.")
            return False
        if self.user_operation.check_username_exist(user_name):
            self.io.print_error_message(
                "CustomerOperation.register_customer", "username already exists.")
            return False
        if not self.validate_email(user_email):
            self.io.print_error_message(
                "CustomerOperation.register_customer", "email is not valid.")
            return False
        if not self.validate_mobile(user_mobile):
            self.io.print_error_message(
                "CustomerOperation.register_customer", "phone number is not valid.")
            return False

        unique_id = self.user_operation.generate_unique_user_id()
        register_time = time.strftime("%d-%m-%Y_%H:%M:%S")
        encrypted_password = self.user_operation.encrypt_password(
            user_password)
        customer = Customer(
            unique_id, user_name, encrypted_password, register_time, user_email=user_email, user_mobile=user_mobile)
        with open("data/users.txt", "a") as file:
            file.write(str(customer) + "\n")
        return True
#Updates the profile information of a customer object based on the specified attribute name and value. Performs validation checks for specific attributes 
#(username, password, email, mobile) before making changes. Updates the changes in the data/users.txt file.
    def update_profile(self, attribute_name, value, customer_object):
        if attribute_name == "user_name":
            #Validate username function in UserOperation class so we will use methods from that class
            if self.user_operation.validate_username(value):
                if not self.user_operation.check_username_exist(value):
                    customer_object.user_name = value
                else:
                    self.io.print_error_message(
                        "CustomerOperation.update_profile", "username already exists.")
                    return False
            else:
                self.io.print_error_message(
                    "CustomerOperation.update_profile", f"invalid username.")
                return False
        elif attribute_name == "user_password":
            if self.user_operation.validate_password(value):
                customer_object.user_password = value
            else:
                self.io.print_error_message(
                    "CustomerOperation.update_profile", "invalid password.")
                return False
        elif attribute_name == "user_email":
            if self.validate_email(value):
                customer_object.user_email = value
            else:
                self.io.print_error_message(
                    "CustomerOperation.update_profile", "email is not valid.")
                return False
        elif attribute_name == "user_mobile":
            if self.validate_mobile(value):
                customer_object.user_mobile = value
            else:
                self.io.print_error_message(
                    "CustomerOperation.update_profile", "phone number is not valid.")
                return False

        customer_object.user_password = self.user_operation.encrypt_password(
            customer_object.user_password)
        #Update changes in the data/users.txt file
        with open("data/users.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            if line.strip().startswith("{'user_id': '" + customer_object.user_id):
                updated_lines.append(str(customer_object) + "\n")
            else:
                updated_lines.append(line)

        with open("data/users.txt", "w", encoding="utf-8") as file:
            file.writelines(updated_lines)

        return True
#Deletes a customer from the data/users.txt file based on the provided customer ID. Searches for the matching customer ID and removes the corresponding line from the file.
    def delete_customer(self, customer_id):
        with open("data/users.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        updated_lines = []
        found = False
        for line in lines:
            if line.strip().startswith("{'user_id': 'u_" + str(customer_id)):
                if ": 'admin'" in line:
                    self.io.print_error_message(
                        "CustomerOperation.delete_customer", "you cannot delete admin user.")
                    return False
                found = True
            else:
                updated_lines.append(line)

        if found:
            with open("data/users.txt", "w", encoding="utf-8") as file:
                file.writelines(updated_lines)
            return True
        else:
            return False
#Retrieves a list of customers from the data/users.txt file for the specified page number. Reads the file, calculates the total number of pages, and extracts the customer data for the requested page.
    def get_customer_list(self, page_number):
        page_size = 10
        with open("data/users.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        total_pages = (len(lines) + page_size - 1) // page_size
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        customer_list = []

        for line in lines[start_index:end_index]:
            #Extract values within '....' using regular expression
            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, line)

            #Remove the values corresponding to dictionary keys
            customer_data = [value.strip("'") for value in values]
            customer = Customer(*customer_data)
            customer_list.append(customer)

        return customer_list, page_number, total_pages

    def delete_all_customers(self):
        admin_line = ""
        with open("data/users.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            if ": 'admin'" in line:
                admin_line = line
                break
        with open("data/users.txt", "w", encoding="utf-8") as file:
            file.write(admin_line)
