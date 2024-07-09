import time
from model_admin import Admin
from operation_customer import UserOperation
from io_interface import IOInterface


class AdminOperation:
    user_operation = UserOperation()
    io = IOInterface()

    def register_admin(self, admin_name, admin_password):
        if not self.user_operation.validate_username(admin_name):
            self.io.print_error_message("AdminOperation.register_admin", "username is not valid.")

            self.io.print_message("The name should only contain letters or underscores, and its length should be at least 5 characters.")
            return False

        #Check if admin account already exists in the database
        if self.user_operation.check_username_exist(admin_name):
            self.io.print_error_message("AdminOperation.register_admin", "username already exists.")
            return False

        if not self.user_operation.validate_password(admin_password):
            self.io.print_error_message("AdminOperation.register_admin", "password is not valid.")

            return False

        #Create a new admin instance
        unique_id = self.user_operation.generate_unique_user_id()
        register_time = time.strftime("%d-%m-%Y_%H:%M:%S")
        encrypted_password = self.user_operation.encrypt_password(
            admin_password)
        admin = Admin(unique_id, admin_name, encrypted_password, register_time)

        #Write admin info into the database
        with open("data/users.txt", "a", encoding="utf-8") as file:
            file.write(str(admin) + "\n")

        return True
