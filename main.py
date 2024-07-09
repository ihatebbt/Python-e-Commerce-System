from io_interface import IOInterface
from operation_admin import AdminOperation
from operation_customer import CustomerOperation
from operation_user import UserOperation
from operation_order import OrderOperation
from operation_product import ProductOperation
from model_admin import Admin
from model_customer import Customer

import random
import string
import time
import os
import re
import matplotlib as plt
import numpy as num

#This function handles the user login process. It prompts the user to enter their username and password, 
#validates the credentials using the user_operation.login() function, and prints a success message if the 
#login is successful.

def login_control():
    username = io.get_user_input("Enter username", 1)[0]
    password = io.get_user_input("Enter password", 1)[0]
    # username = "testing"
    # password = "testing"

    result = user_operation.login(username, password)
    if result is not None:
        io.print_message("You are logged in successfully.")
    return result

#This function collects customer information for registration. It prompts the user to enter a username, password, 
#and email address, and verifies that the password is entered correctly. It then calls the customer_operation.register_customer() 
#function to register the customer with the provided information and prints a success message if the registration is successful.
def take_customer_info():
    username = io.get_user_input("Enter username", 1)[0]
    password = io.get_user_input("Enter password", 1)[0]
    password_again = io.get_user_input("Enter password again", 1)[0]
    if password_again != password:
        io.print_error_message("main.take_customer_info", "passwords do not match.")
        return

    email = io.get_user_input("Enter email address", 1)[0]
    phone = io.get_user_input("Enter phone number", 1)[0]

    res = customer_operation.register_customer(
        username, password, email, phone)
    if res:
        io.print_message("Customer successfully registered.")

#This function manages the update profile menu for a logged-in user. It displays the update profile menu options,  prompts the user to choose an option, 
#and performs the corresponding update based on the selected option. The function updates the user's username, password, email, or mobile number using 
#the customer_operation.update_profile() function. It also updates the corresponding attributes of the user object. If the user chooses to exit the menu, 
#the function returns the updated user object.

def update_form_control(user):
    while True:
        io.update_profile_menu()
        sub_menu_option = io.get_user_input("Please enter your choice", 1)[0]
        if sub_menu_option == "5":
            return user
        elif sub_menu_option == "1":
            new_user_name = io.get_user_input("Enter new username", 1)[0]
            res = customer_operation.update_profile(
                "user_name", new_user_name, user)
            if res:
                io.print_message("Successfully updated username")
                user.user_name = new_user_name
        elif sub_menu_option == "2":
            password, password_again = io.get_user_input("Enter 2 times new password with a space", 2)

            if password != password_again:
                io.print_error_message("main.update_form_control.sub_option_2", "Passwords do not match.")
                continue
            res = customer_operation.update_profile("user_password", password, user)
            if res:
                io.print_message("Successfully updated password.")
                user.user_password = password
        elif sub_menu_option == "3":
            new_user_email = io.get_user_input("Enter new email", 1)[0]
            res = customer_operation.update_profile(
                "user_email", new_user_email, user)
            if res:
                io.print_message("Successfully updated email")
                user.user_email = new_user_email

        elif sub_menu_option == "4":
            new_user_mobile = io.get_user_input("Enter new mobile", 1)[0]
            res = customer_operation.update_profile(
                "user_mobile", new_user_mobile, user)
            if res:
                io.print_message("Successfully updated mobile")
                user.user_mobile = new_user_mobile

        else:
            io.print_error_message('main.update_form_control', "invalid choice entered for menu")

#This function handles the control flow and user interactions for the customer interface. It displays the customer menu options and prompts the user to enter a choice. 
#Based on the choice, it performs actions such as displaying customer information, updating the customer's profile, searching for products, viewing order history, generating 
#consumption figures, and viewing product details.
def customer_control(logged_in_user):
    while True:
        #Display Customer Menu Options
        io.customer_menu()
        sub_menu_option = io.get_user_input("Please enter your choice", 1)[0]
        if sub_menu_option == "7":
            io.print_message("You are logged out.")
            break
        elif sub_menu_option == "1":
            io.print_customer_object(logged_in_user)
        elif sub_menu_option == "2":
            logged_in_user = update_form_control(logged_in_user)
        elif sub_menu_option == "3":
            #Prompt the user to enter search keywords
            keyword = io.get_user_input("Enter 1 or 2 keywords", 2)
            #Combine the keywords into a single string
            keyword = " ".join(keyword).strip()

            res = product_operation.get_product_list_by_keyword(keyword)
            header_length, header_values, table_data_format = io.get_product_table_data()
            io.print_table(header_values, (res, ),
                           header_length, table_data_format, False)
        elif sub_menu_option == "4":
            #Get the customer's order list
            orders_data = order_operation.get_order_list(
                logged_in_user.user_id, 1)
            if len(orders_data[0]) == 0:
                io.print_message("There are no orders for this customer.")
                continue
            io.print_message(f"Total Pages: {orders_data[-1]}")
            pages = io.get_user_input("Please enter page number of page range like, 5 or 2 5", 2)
            #Convert input to start and end page numbers
            start, end = [0 if x == '' else int(x) for x in pages]
            if end == 0:
                start, end = start-1, start
            else:
                start -= 1
            for i in range(start, end):
                data = order_operation.get_order_list(
                    logged_in_user.user_id, i+1)
                io.show_list('admin', 'Order', data)
        elif sub_menu_option == "5":
            io.print_message("Generating all consumption figures, please wait.")
            order_operation.generate_single_customer_consumption_figure(
                logged_in_user.user_id)
            io.print_message("All consumption figures has been generated.")
        elif sub_menu_option == '6':
            try:
                product_id = int(io.get_user_input("Enter Product ID", 1)[0])
            except ValueError:
                io.print_error_message("main.customer_control.sub_option_6", "Please enter product ID in numbers only")
                continue

            res = product_operation.get_product_by_id(str(product_id))
            header_length, header_values, table_data_format = io.get_product_table_data()
            io.print_table(header_values, ([str(res)], ),
                           header_length, table_data_format, False)
        else:
            io.print_error_message('main.customer_control', "invalid choice entered for menu")

#This function handles the control flow and user interactions for the admin interface. It displays the admin menu options and prompts the user 
#to enter a choice. Based on the choice, it performs actions such as viewing product lists, registering new customers, viewing customer lists, 
#viewing customer order history, generating test data, generating statistical data, deleting all data, deleting a customer, deleting an order, 
#and deleting a product.
def admin_control():
    while True:
        io.admin_menu() #Get User's Input
        sub_menu_option = io.get_user_input("Please enter your choice", 1)[0]
        # sub_menu_option = "4"
        if sub_menu_option == "11":
            io.print_message("You are logged out.")
            break
        elif sub_menu_option == '1':
            orders_data = product_operation.get_product_list(0)[-1] #Display Product List
            io.print_message(f"Total Pages: {orders_data}")
            pages = io.get_user_input("Please enter page number of page range like, 5 or 2 5", 2) #Get Page Number
            start, end = [0 if x == '' else int(x) for x in pages]
            if end == 0:
                start, end = start-1, start
            else:
                start -= 1
            for i in range(start, end): #Iterate over the pages to display product data
                data = product_operation.get_product_list(i+1)
                io.show_list('admin', 'Product', data)
        elif sub_menu_option == '2':
            take_customer_info() #This takes customer information
        elif sub_menu_option == '3':
            orders_data = customer_operation.get_customer_list(0)[-1]
            io.print_message(f"Total Pages: {orders_data}")
            pages = io.get_user_input("Please enter page number of page range like, 5 or 2 5", 2)
            start, end = [0 if x == '' else int(x) for x in pages]
            if end == 0:
                start, end = start-1, start
            else:
                start -= 1
            for i in range(start, end):
                data = customer_operation.get_customer_list(i+1) #Iteration again over the specified pages and customer data
                io.show_list('admin', 'Customer', data)
        elif sub_menu_option == '4':
            try:
                user_id = int(io.get_user_input("Enter Customer ID", 1)[0])
            except ValueError:
                io.print_error_message("main.admin_control.sub_option_4", "Please enter user ID in numbers only")
                continue
            orders_data = order_operation.get_order_list(user_id, 1)
            if len(orders_data[0]) == 0:
                io.print_message("There are no orders for this customer.")
                continue
            io.print_message(f"Total Pages: {orders_data[-1]}")
            pages = io.get_user_input("Please enter page number of page range like, 5 or 2 5", 2)
            start, end = [0 if x == '' else int(x) for x in pages]
            if end == 0:
                start, end = start-1, start
            else:
                start -= 1
            for i in range(start, end): #Iteration over the pages and display order data
                data = order_operation.get_order_list(user_id, i+1)
                io.show_list('admin', 'Order', data)
        elif sub_menu_option == '5':
            io.print_message("Generating test data, please wait.")
            order_operation.generate_test_order_data()
            io.print_message("Test data has been generated.")
        elif sub_menu_option == '6':
            io.print_message("Generating statistical data, please wait.")
            order_operation.generate_all_top_10_best_sellers_figure()
            product_operation.generate_category_figure()
            product_operation.generate_discount_figure()
            product_operation.generate_discount_likes_count_figure()
            product_operation.generate_likes_count_figure()
            io.print_message("Statistical data has been generated.")
        elif sub_menu_option == '7':
            sure = io.get_user_input("Are you sure you want to delete all data? Press 'y' for yes", 1)[0]
            if sure.lower() == 'y':
                order_operation.delete_all_orders()
                product_operation.delete_all_products()
                customer_operation.delete_all_customers()
                io.print_message("All data has been deleted.")
        elif sub_menu_option == '8':
            try:
                user_id = int(io.get_user_input("Enter Customer ID", 1)[0])
            except ValueError:
                io.print_error_message("main.admin_control.sub_option_8", "Please enter user ID in numbers only")
                continue
            sure = io.get_user_input("Are you sure you want to delete this customer? Press 'y' for yes", 1)[0]
            if sure.lower() == 'y':
                res = customer_operation.delete_customer(str(user_id))
                if res:
                    io.print_message("Customer has been deleted.")
                else:
                    io.print_message("Customer ID does not found.")
        elif sub_menu_option == '9':
            try:
                order_id = int(io.get_user_input("Enter Order ID", 1)[0])
            except ValueError:
                io.print_error_message("main.admin_control.sub_option_9", "Please enter order ID in numbers only")
                continue
            sure = io.get_user_input("Are you sure you want to delete this order? Press 'y' for yes", 1)[0]
            if sure.lower() == 'y':
                res = order_operation.delete_order(str(order_id))
                if res:
                    io.print_message("Order has been deleted.")
                else:
                    io.print_message("Order ID does not found.")
        elif sub_menu_option == '10':
            try:
                product_id = int(io.get_user_input("Enter Product ID", 1)[0])
            except ValueError:
                io.print_error_message("main.admin_control.sub_option_10", "Please enter product ID in numbers only")
                continue
            sure = io.get_user_input("Are you sure you want to delete this product? Press 'y' for yes", 1)[0]
            if sure.lower() == 'y':
                res = product_operation.delete_product(str(product_id))
                if res:
                    io.print_message("Product has been deleted.")
                else:
                    io.print_message("Product ID does not found.")
        else:
            io.print_error_message('main.admin_control', "invalid choice entered for menu")

#This is the main function that runs the program. It initializes the necessary objects and operations, displays the main menu options, 
#prompts the user to enter a choice, and based on the choice, it calls the appropriate functions for the admin or customer interface. 
#It also includes the initial setup by registering an admin with a default username and password.
def main():
    logged_in = None
    while True:
        io.main_menu()
        main_menu_option = io.get_user_input("Please enter your choice", 1)[0]
        #main_menu_option = "1"
        if main_menu_option == "3":
            break
        elif main_menu_option == '1':
            res = login_control()
            if isinstance(res, Admin):
                logged_in = res

                admin_control()
            elif isinstance(res, Customer):
                logged_in = res

                customer_control(logged_in)
            else:
                logged_in = res

        elif main_menu_option == '2':
            pass
        else:
            io.print_error_message('main', "invalid choice entered for main menu")
        main_menu_option = "3"


if __name__ == '__main__':
    io = IOInterface()
    admin_operation = AdminOperation()
    customer_operation = CustomerOperation()
    user_operation = UserOperation()
    order_operation = OrderOperation()
    product_operation = ProductOperation()

    admin_operation.register_admin('admin', 'admin1')
    main()
