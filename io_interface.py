import re

class IOInterface:
    def get_user_input(self, message, num_of_args):
        user_input = input(message+': ').split()
        if len(user_input) > num_of_args:
            user_input = user_input[:num_of_args]
        else:
            remaining = num_of_args - len(user_input)
            user_input += ['']*remaining
        return user_input

    def main_menu(self):
        print("**Login Menu**")
        print("(1) Login")
        print("(2) Register")
        print("(3) Quit")
    def admin_menu(self):
        print("**Admin Menu**")
        print("(1) Show products")
        print("(2) Add Customer")
        print("(3) Show Customer")
        print("(4) Show Orders")
        print("(5) Generate Test Data")
        print("(6) Generate Statistical Figures")
        print("(7) Delete All Data")
        print("(8) Delete Customer Using Customer ID")
        print("(9) Delete Order Using Order ID")
        print("(10) Delete Product Using Product ID")
        print("(11) Logout")
    def customer_menu(self):
        print("**Customer Menu**")
        print("(1) Show profile")
        print("(2) Update Profile")
        print("(3) Show Products (user input could be “3 keyword” or “3”)")
        print("(4) Show History orders")
        print("(5) Generate All Consumption Figures")
        print("(6) Get Product Using Product ID")
        print("(7) Logout")       
    def update_profile_menu(self):
        print("**Customer Update Profile Menu**")
        print("(1) Username")
        print("(2) Password")
        print("(3) Email")
        print("(4) Mobile")
        print("(5) Back")
#Displays a list of objects in a tabular format based on the given user role and list type. If the user role is 'customer' and the list 
#type is not 'Product' or 'Order', it denies access and prints an error message. If the object list is empty, it returns without displaying anything.
#Determines the table structure based on the list type and formats the header and table lines. Prints the header, data rows, and footer of the table.
    def show_list(self, user_role, list_type, object_list):
        if user_role == 'customer':
            if list_type not in ["Product", "Order"]:
                print("You are not allowed to see the given list.")
                return
        if len(object_list[0]) == 0:
            return
        header_values = []
        if list_type == 'Customer':
            header_length  = [10,14,20,60,22,13,30,13]
            customer_header = ["Row Number", "user_id", "user_name", "user_password", "user_register_time", "user_role", "user_email", "user_mobile"]
            table_data_format = "|{:^10}|{:^14}|{:^20}|{:^60}|{:^22}|{:^13}|{:^30}|{:^13}|"
            header_values = customer_header
        elif list_type == 'Product':
            header_length, header_values, table_data_format= self.get_product_table_data()
        
        elif list_type == 'Order':
            header_length  = [10,10,14,10,22]
            order_header = ["Row Number", "order_id", "user_id", "pro_id", "order_time"]
            table_data_format = "|{:^10}|{:^10}|{:^14}|{:^10}|{:^22}|"
            header_values = order_header

        header_values = [x.replace("_", " ").title() for x in header_values]

        header = table_data_format.format(*header_values)
        table_line = '-'* len(header)
        self.print_table(header_values, object_list, header_length, table_data_format)

        footer_text = f"Page Number: {object_list[1]}, out of {object_list[-1]}"
        footer_length = len(table_line)-2
        print("|{:^{}}|".format(footer_text, footer_length))
        print(f"{table_line}\n")
#Returns the header length, header values, and table data format specific to the 'Product' list type. Defines the header length, header values, 
#and table data format for the 'Product' table. Formats the header values. Returns the defined values.
    def get_product_table_data(self):
        header_length  = [10,10,15,15,60,17,15,13, 18]
        product_header = ["Row Number", "pro_id", "pro_model", "pro_category", "pro_name", "pro_current_price", "pro_raw_price", "pro_discount", "pro_likes_count"]
        table_data_format = "|{:^10}|{:^10}|{:^15}|{:^15}|{:^60}|{:^17}|{:^15}|{:^13}|{:^18}|"

        header_values = [x.replace("_", " ").title() for x in product_header]

        return header_length, header_values, table_data_format
#Prints a table with the given header values and object list in a formatted manner. Formats the header and table lines using the table data format. 
#Iterates over the object list and extracts values to be displayed in each row. Removes the values corresponding to dictionary keys. 
#Prints the formatted table rows. Prints the table lines.
    def print_table(self, header_values, object_list, header_length, table_data_format, current_method=True):
        header = table_data_format.format(*header_values)
        table_line = '-'* len(header)
        print(table_line)
        print(header)
        print(table_line)

        
        for i, each in enumerate(object_list[0], 1):
            if current_method:
                row_num = i+((object_list[1]-1)*10)
            else:
                row_num = i

            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, str(each))

            #Remove the values corresponding to dictionary keys
            values = [values[i].strip("'")[:header_length[i+1]] for i in range(len(values))]
            values.insert(0, row_num)
            #print(values)

            print(table_data_format.format(*values))
        print(table_line)
#Prints an error message with the given error source and error message. Prints an error message indicating the source and details of the error.
    def print_error_message(self, error_source, error_message):
        print(f"{error_source}: {error_message}")
    
    def print_message(self, message):
        print(message)
#Prints the attributes and their corresponding values of a customer object. Retrieves the customer object attributes.   
    def print_customer_object(self, target_object):
        customer_header = ["user_id", "user_name", "user_password", "user_register_time", "user_role", "user_email", "user_mobile"]
        header_values = [x.replace("_", " ").title() for x in customer_header]

        for i in range(len(customer_header)):
            val = getattr(target_object, customer_header[i])
            print(f"{header_values[i]}: {val}")

        
