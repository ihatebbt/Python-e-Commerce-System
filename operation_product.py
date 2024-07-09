import os
import matplotlib.pyplot as plt
import csv
import re

from model_product import Product


class ProductOperation:
    DATA_FOLDER = "data"
    PRODUCT_INFO_FILE = os.path.join(DATA_FOLDER, "products.txt")
    FIGURE_FOLDER = os.path.join(DATA_FOLDER, "figure")
#unction extracts product information from CSV files located in a specified folder. It reads each file, 
#parses the data using regular expressions, creates Product objects, and appends them to a list. The list 
#is then saved to a text file.
    def extract_products_from_files(self):
        source_folder = os.path.join(self.DATA_FOLDER, "product")
        csv_files = [file for file in os.listdir(
            source_folder) if file.endswith(".csv")]
#csv_files = [file for file in os.listdir(
#source_folder) if file.endswith("shoes.csv")]
#Use regular expressions to extract values
        pattern = r'("(?:[^"]|"")*"|[^,]*)'

        product_list = []

        for file in csv_files:
            file_path = os.path.join(source_folder, file)
            with open(file_path, "r") as csv_file:
                lines = csv_file.readlines()
        #         next(lines)
        #         i = 0
                for line in lines[1:]:
                    values = re.findall(pattern, line.strip())
                    data = [x.strip('"') for x in values if x]
                    try:
                        pro_id = data[-2]
                        pro_model = data[-1]
                        pro_category = data[0]
                        pro_name = data[2]
                        pro_current_price = float(data[3])
                        pro_raw_price = float(data[4])
                        pro_discount = int(data[6])
                        pro_likes_count = int(data[7])
                    except:
                        print(data)
                        return

                    product = Product(pro_id, pro_model, pro_category, pro_name, pro_current_price,
                                      pro_raw_price, pro_discount, pro_likes_count)
                    # i += 1
                    product_list.append(product)

        with open(self.PRODUCT_INFO_FILE, "w") as file:
            for product in product_list:
                file.write(str(product) + "\n")
#This function retrieves a list of products based on the specified page number. It reads the product information 
#from the text file, calculates the total number of pages, and returns a sublist of products for the given page number.
    def get_product_list(self, page_number):
        page_size = 10
        with open(self.PRODUCT_INFO_FILE, "r") as file:
            lines = file.readlines()

        total_pages = (len(lines) + page_size - 1) // page_size
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        product_list = []

        for line in lines[start_index:end_index]:
            #Extract values within '....' using regular expression
            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, line)

            #Remove the values corresponding to dictionary keys
            product_data = [value.strip("'") for value in values]
            product = Product(*product_data)
            product_list.append(product)

        return product_list, page_number, total_pages
#This function deletes a product from the list based on the provided product ID. It reads the product information from the text file, 
#searches for the product with the given ID, removes it from the list, and updates the text file.
    def delete_product(self, product_id):
        with open(self.PRODUCT_INFO_FILE, "r") as file:
            lines = file.readlines()

        updated_lines = []
        found = False
        for line in lines:
            if line.strip().startswith("{'pro_id': '" + product_id):
                found = True
            else:
                updated_lines.append(line)

        if found:
            with open(self.PRODUCT_INFO_FILE, "w") as file:
                file.writelines(updated_lines)
            return True
        else:
            return False
#This function retrieves a list of products that contain the provided keyword in their names. It reads the product information from the text file, 
#searches for products whose names match the keyword (case-insensitive), creates Product objects, and returns the filtered list.
    def get_product_list_by_keyword(self, keyword):
        with open(self.PRODUCT_INFO_FILE, "r") as file:
            lines = file.readlines()

        keyword = keyword.lower()
        product_list = []

        for line in lines:
            #Extract values within '....' using regular expression
            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, line)

            #Remove the values corresponding to dictionary keys
            product_data = [value.strip("'") for value in values]
            #as pro_name is on 3rd index so we use that here
            if keyword in product_data[3].lower():
                product = Product(*product_data)
                product_list.append(product)

        return product_list
#This function retrieves a product based on the provided product ID. It reads the product information from the text file, searches for the product with the given ID, 
#creates a Product object, and returns it. If no product is found, it returns None.
    def get_product_by_id(self, product_id):
        with open(self.PRODUCT_INFO_FILE, "r") as file:
            lines = file.readlines()

        for line in lines:
            if line.strip().startswith("{'pro_id': '" + product_id):
                #Extract values within '....' using regular expression
                pattern = r": ('.*?')[,}]"
                values = re.findall(pattern, line)

                #Remove the values corresponding to dictionary keys
                product_data = [value.strip("'") for value in values]
                return Product(*product_data)

        return None
#This function generates a bar chart showing the count of products in each category. It reads the product information from the text file, counts the products 
#in each category, sorts the categories based on count, and plots the bar chart using matplotlib. The chart is saved as an image file.
    def generate_category_figure(self):
        with open(self.PRODUCT_INFO_FILE, "r") as file:
            lines = file.readlines()

        category_counts = {}
        for line in lines:
            #Extract values within '....' using regular expression
            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, line)

            #Remove the values corresponding to dictionary keys
            product_data = [value.strip("'") for value in values]

            #pro_category is at 2nd index
            category = product_data[2]
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1

        sorted_categories = sorted(
            category_counts, key=lambda x: category_counts[x], reverse=True)
        categories = []
        counts = []
        for category in sorted_categories:
            categories.append(category)
            counts.append(category_counts[category])

        plt.figure(figsize=(15, 15))
        plt.bar(categories, counts)
        plt.xticks(rotation=45)
        plt.xlabel("Category")
        plt.ylabel("Count")
        plt.title("Product Categories")
        plt.savefig(os.path.join(self.FIGURE_FOLDER,
                    "generate_category_figure.png"))
        plt.close()
#This function generates a pie chart showing the proportions of products with different discount ranges. It reads the product 
#information from the text file, categorizes the discounts into three ranges, counts the products in each range, and plots the 
#pie chart using matplotlib. The chart is saved as an image file.
    def generate_discount_figure(self):
        with open(self.PRODUCT_INFO_FILE, "r") as file:
            lines = file.readlines()

        less_than_30 = 0
        between_30_and_60 = 0
        greater_than_60 = 0

        for line in lines:
            #Extract values within '....' using regular expression
            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, line)

            #Remove the values corresponding to dictionary keys
            product_data = [value.strip("'") for value in values]
            #pro_discount is at 2nd last index
            discount = float(product_data[-2])
            if discount < 30:
                less_than_30 += 1
            elif discount >= 30 and discount <= 60:
                between_30_and_60 += 1
            else:
                greater_than_60 += 1

        labels = ["<30", "30-60", ">60"]
        sizes = [less_than_30, between_30_and_60, greater_than_60]
        colors = ["red", "yellow", "green"]

        plt.figure(figsize=(15, 15))
        plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%")
        plt.title("Discount Proportions")
        plt.legend()
        plt.savefig(os.path.join(self.FIGURE_FOLDER,
                    "generate_discount_figure.png"))
        plt.close()
#Simliar to the the generate discount figure, This function generates a line plot showing the likes count for each category. It reads the product information from 
#the text file, sums the likes counts for each category, sorts the categories based on likes count, and plots the line chart using matplotlib. The chart is saved 
#as an image file.
    def generate_likes_count_figure(self):
        with open(self.PRODUCT_INFO_FILE, "r") as file:
            lines = file.readlines()

        category_likes = {}
        for line in lines:
            #Extract values within '....' using regular expression
            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, line)

            #Remove the values corresponding to dictionary keys
            product_data = [value.strip("'") for value in values]
            #pro_category is at 2nd index
            category = product_data[2]

            #pro_likes_count is at last index
            likes_count = int(product_data[-1])
            if category in category_likes:
                category_likes[category] += likes_count
            else:
                category_likes[category] = likes_count

        sorted_categories = sorted(
            category_likes, key=lambda x: category_likes[x])
        categories = []
        likes = []
        for category in sorted_categories:
            categories.append(category)
            likes.append(category_likes[category])

        plt.figure(figsize=(15, 15))
        plt.plot(categories, likes, marker="o")
        plt.xticks(rotation=45)
        plt.xlabel("Category")
        plt.ylabel("Likes Count")
        plt.title("Likes Count by Category")
        plt.savefig(os.path.join(self.FIGURE_FOLDER,
                    "generate_likes_count_figure.png"))
        plt.close()
#very similar concept as the other two generating figures
    def generate_discount_likes_count_figure(self):
        with open(self.PRODUCT_INFO_FILE, "r") as file:
            lines = file.readlines()

        discounts = []
        likes_counts = []
        for line in lines:
            # Extract values within '....' using regular expression
            pattern = r": ('.*?')[,}]"
            values = re.findall(pattern, line)

            # Remove the values corresponding to dictionary keys
            product_data = [value.strip("'") for value in values]
            # pro_discount is at 2nd last index
            discount = float(product_data[-1])

            # pro_likes_count is at last index
            likes_count = int(product_data[-1])

            discounts.append(discount)
            likes_counts.append(likes_count)

        plt.figure(figsize=(15, 15))
        plt.scatter(discounts, likes_counts)
        plt.xlabel("Discount")
        plt.ylabel("Likes Count")
        plt.title("Discount vs Likes Count")
        plt.savefig(os.path.join(self.FIGURE_FOLDER,
                    "generate_discount_likes_count_figure.png"))
        plt.close()
#deletes all products from the list by clearing the content of the text file.
    def delete_all_products(self):
        with open(self.PRODUCT_INFO_FILE, "w") as file:
            file.write("")
