from model_user import User

#It inherits the attributes and methods from the User class using the super() function in the __init__ method
#The __init__ method of the Admin class takes the required arguments for the user ID, user name, user password, 
#user register time, and user role. It calls the __init__ method of the User class using super() and provides the necessary arguments


class Admin(User):
    def __init__(self, user_id, user_name, user_password, user_register_time="00-00-0000_00:00:00", user_role="admin"):
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)

    def __str__(self):
        return f"{super().__str__()[:-1]}}}"