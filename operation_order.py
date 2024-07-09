import random
import string
import time
import os
import re
import matplotlib.pyplot as plt
from model_order import Order
from operation_customer import CustomerOperation
from operation_user import UserOperation
from model_customer import Customer
from operation_product import ProductOperation


class OrderOperation:
    DATA_FOLDER = "data"
    ORDER_INFO_FILE = os.path.join(DATA_FOLDER, "orders.txt")
    FIGURE_FOLDER = os.path.join(DATA_FOLDER, "figure")
    user_operation = UserOperation()
    product_operation = ProductOperation()
    customer_operation = CustomerOperation()
#Generates a unique order ID starting with "o_" followed by a 5-digit random number. method generates a unique order ID by appending a 
#random 5-digit number to the prefix "o_". It checks the uniqueness of the generated ID by calling the check_unique_order_id_exist() method
    def generate_unique_order_id(self):
        while True:
            unique_id = "o_" + ''.join(random.choices(string.digits, k=5))
            if not self.check_unique_order_id_exist(unique_id):
                return unique_id
#Checks if a given order ID already exists in the orders.txt file. method reads the contents of the orders.txt file and checks if any line starts 
#with the provided order ID. If a match is found, it returns True, indicating that the order ID already exists.
    def check_unique_order_id_exist(self, order_id):
        with open(self.ORDER_INFO_FILE, "r", encoding="utf-8") as file:
            #read all lines in the file
            order_data = file.readlines()
            for line in order_data:
                if line.strip().startswith("{'order_id': '" + order_id):
                    return True
            return False
#Creates a new order with the provided customer ID, product ID, and optional creation time. The order is written to the orders.txt file. method creates 
#a new Order object with a unique order ID, the provided customer ID, product ID, and an optional creation time. The order object is then written to the 
#orders.txt file.
    def create_an_order(self, customer_id, product_id, create_time=None):
        if create_time is None:
            create_time = time.strftime("%d-%m-%Y_%H:%M:%S")

        unique_id = self.generate_unique_order_id()
        order = Order(unique_id, customer_id, product_id, create_time)
        with open("data/orders.txt", "a", encoding="utf-8") as file:
            file.write(str(order) + "\n")

            return True
#Deletes an order with the given order ID from the orders.txt file. method deletes an order from the orders.txt file by reading all lines, excluding the line 
#with the provided order ID, and rewriting the remaining lines.
    def delete_order(self, order_id):
        with open(self.ORDER_INFO_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        updated_lines = []
        found = False
        for line in lines:
            if line.strip().startswith("{'order_id': 'o_" + order_id):
                found = True
            else:
                updated_lines.append(line)

        if found:
            with open(self.ORDER_INFO_FILE, "w", encoding="utf-8") as file:
                file.writelines(updated_lines)
            return True
        else:
            return False
#Retrieves a list of all orders. If a customer ID is provided, it filters the orders for that specific customer. retrieves a list of all orders from the orders.txt file. 
#If a customer ID is provided, it filters the orders to only include those belonging to the specified customer.
    def get_all_orders_list(self, customer_id=None):
        with open(self.ORDER_INFO_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
        order_list = []
        for line in lines:
            #Extract values within '....' using regular expression
            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, line)

            #Remove the values corresponding to dictionary keys
            order_data = [value.strip("'") for value in values]
            if customer_id is None or customer_id in order_data:
                order = Order(*order_data)
                order_list.append(order)

        return order_list
#Retrieves a list of orders for a specific customer, divided into pages. The page number determines which subset of orders to retrieve. method retrieves a list of orders
# or a specific customer, divided into pages. It reads all lines from the orders.txt file, filters the orders based on the customer ID, and returns a subset of orders 
#based on the page number and page size.
    def get_order_list(self, customer_id, page_number):
        page_size = 10
        with open(self.ORDER_INFO_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
        order_list = []
        for line in lines:
            #Extract values within '....' using regular expression
            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, line)

            #Remove the values corresponding to dictionary keys
            order_data = [value.strip("'") for value in values]
            if str(customer_id) in order_data[1]:
                order = Order(*order_data)
                order_list.append(order)

        total_pages = (len(order_list) + page_size - 1) // page_size
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        order_list = order_list[start_index:end_index]

        return order_list, page_number, total_pages
#Generates test order data by creating random orders for customers and random products. method generates test order data for customers. It ensures that there are at least 10 
#customers and creates random orders for each customer by selecting random products and setting random order times within a desired month.
    def generate_test_order_data(self):
        user_name = 'testing_'
        password = 'testing_123_'

        cust_data = self.customer_operation.get_customer_list(1)

        if len(cust_data[0]) < 10:
            for i in range(10-len(cust_data[0])):
                cur_user_name = user_name+string.ascii_lowercase[i]
                cur_password = password+string.ascii_lowercase[i]
                cur_email = cur_user_name+"@monash.edu"
                cur_phone = '04' + ''.join(random.choices(string.digits, k=8))

                self.customer_operation.register_customer(
                    cur_user_name, cur_password, cur_email, cur_phone)

        self.product_operation.delete_all_products()
        self.product_operation.extract_products_from_files()

        pro_all_pages = self.product_operation.get_product_list(0)[-1]

        customers = cust_data[0]

        for customer in customers:
            random_product_count = random.randint(50, 200)
            #print("CUSTOMER", customer.user_id, random_product_count)
            for i in range(random_product_count):
                products = self.product_operation.get_product_list(
                    random.randint(1, pro_all_pages))[0]

                random_product = random.choice(products)

                #controlling order time month
                #Set the desired month
                desired_month = random.randint(1, 12)

                #Get the current time as a struct_time object
                current_time = time.localtime()

                #Extract the year and day from the struct_time object
                current_year = current_time.tm_year
                current_day = current_time.tm_mday

                #Create a new struct_time object with the desired month
                desired_time = time.struct_time((current_year, desired_month, current_day, current_time.tm_hour, current_time.tm_min,
                                                current_time.tm_sec, current_time.tm_wday, current_time.tm_yday, current_time.tm_isdst))
                desired_time = time.strftime("%d-%m-%Y_%H:%M:%S", desired_time)

                self.create_an_order(
                    customer.user_id, random_product.pro_id, desired_time)
 #Generates a bar graph showing the consumption (sum of order prices) for each month for a specific customer.  method generates a bar graph showing the consumption 
 #(sum of order prices) for each month for a specific customer. It retrieves all orders for the customer, calculates the total price for each month, and plots the 
 #data using matplotlib.pyplot.
    def generate_single_customer_consumption_figure(self, customer_id):
        all_orders = self.get_all_orders_list(customer_id)

        graph_data = {i: 0 for i in range(1, 13)}

        for order in all_orders:
            if order.user_id != customer_id:
                continue
            product = self.product_operation.get_product_by_id(
                order.pro_id)
            price = product.pro_current_price
            month = time.strptime(
                order.order_time, "%d-%m-%Y_%H:%M:%S").tm_mon

            graph_data[month] = graph_data.get(month, 0) + float(price)
        #Extract the keys and values from the dictionary
        labels = list(graph_data.keys())
        data = list(graph_data.values())
        plt.bar(labels, data)
        plt.xticks(labels)
        plt.xlabel("Months")
        plt.ylabel("Consumption")
        plt.title("The consumption(sum of order price) of 12 different months")
        plt.savefig(os.path.join(self.FIGURE_FOLDER,
                    "generate_single_customer_consumption_figure.png"))
        plt.close()
#Generates a bar graph showing the top 10 best-selling products based on the total count of orders.
    def generate_all_top_10_best_sellers_figure(self):
        all_orders = self.get_all_orders_list()
        graph_data = {}

        for order in all_orders:
            graph_data[order.pro_id] = graph_data.get(order.pro_id, 0) + 1

        sorted_data = sorted(graph_data.items(), key=lambda x: x[-1])[-10:]
        #Extract the keys and values from the dictionary
        labels = [x[0] for x in sorted_data]
        data = [x[1] for x in sorted_data]

        plt.figure(figsize=(15, 15))
        plt.bar(labels, data)
        plt.xticks(labels, rotation=45)
        plt.xlabel("Products")
        plt.ylabel("Counts")
        plt.title("The top 10 best-selling products")
        plt.savefig(os.path.join(self.FIGURE_FOLDER,
                    "generate_all_top_10_best_sellers_figure.png"))
        plt.close()
#Deletes all orders by clearing the contents of the orders.txt file.
    def delete_all_orders(self):
        with open(self.ORDER_INFO_FILE, "w", encoding="utf-8") as file:
            file.write("")
