from model_user import User
#Used the super() function in __init__ to inherit the attributes methods from User class
#The __init__ method of customer class adds two additional arguments, used super() in the return statement
#of __str__ so that it calls the method of the User class then appends the user_email and user_mobile attributes


class Customer(User):
    def __init__(self, user_id, user_name, user_password, user_register_time="00-00-0000_00:00:00", user_role="customer", user_email="", user_mobile=""):
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)
        self.user_email = user_email
        self.user_mobile = user_mobile

    def __str__(self):
        return f"{super().__str__()[:-1]}, 'user_email': '{self.user_email}', 'user_mobile': '{self.user_mobile}'}}"
