"""
Madeline Berardi
400643493

Kavya Sachdeva
400643277

Alp Jashanica
400625572

Sara Bilal
400624902

Kabir Singh Dillon
400625526

Creates a warehouse system for users to purchase products and have the Qarm pack them. This includes creating an account, processing the order, and summarizing a receipt.
"""

##Imports

import csv  # lets you read/write CSV
import os   # To check if os.path.isfile exists
import bcrypt # Used to hash passwords
import random

##Global Variables

LEGAL_SYMBOLS = set("!.@#$%^&*()_[]") # allowed set symbols. set makes sure that the symbols are valid for the password

##Sign Up

def file_exists(path):
    """Sara Bilal: Returns true or false, os.path.isfile is used to check if the file is present or not"""
    return os.path.isfile(path)


def load_users():
    """Sara Bilal: loads users and the hashed password"""
    users = {} # initializes empty dictionary
    if file_exists("users.csv"): #opens file in readmode
        with open("users.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f) # turns file into rows
            for row in reader:
                if len(row) >= 2: # insures there are at least two columns
                    userid, encrypted_password = row[0], row[1] ## 0= user, 1=password
                    users[userid] = encrypted_password
    return users


def append_user(userid, encrypted_password):
    """Sara Bilal: creates a file if not alredy made, every time a new account is created there is a new row of username and password added"""
    with open("users.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([userid, encrypted_password])


def is_valid_password(password):
    """Sara Bilal: Checks if the password is valid"""
    if len(password) < 6:
        return False

    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_symbol = any(ch in LEGAL_SYMBOLS for ch in password)

    return has_upper and has_lower and has_digit and has_symbol

def sign_up():
    """Sara Bilal: Makes a new account, checks if the user is alredy in the system, if they arn'r it asks for a username and loops if the user is alredy taken etc"""
    print("Sign up")

    users = load_users()

    while True:
        userid = input("Enter a new userid: ").strip()

        if userid == "":
            print("Userid cannot be empty.try again.")
            continue

        if userid in users:
            print("That userid already exists.")
        else:
            break

    print("Your password must:")
    print("- be at least 6 characters")
    print("- contain one uppercase letter")
    print("- contain one lowercase letter")
    print("- contain one digit")
    print(f"- contain one symbol from {''.join(sorted(LEGAL_SYMBOLS))}")

    while True:
        password = input("Enter a new password: ")
        if not is_valid_password(password):
            print("Password invalid. try again.")
        else:
            break

    hash_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) #Password string turned into bytes
    encrypted_password = hash_bytes.decode("utf-8") #Bytes tuned into string to store in CSV

    append_user(userid, encrypted_password) # adds user to the file

    print(f"Account created")

##Authenticate

def authenticate():

    """Kabir Singh Dillon: Function that handles user sign-in, checking whether a userId exists and if the correspong password entered by the user is correct. If successful the function returns the user's Id"""

    # Main authentication loop that continues until a successful login or sign-up
    while True:
        # Ask user if they already have an account
        user = input("Do you have an account? (Yes/No): ").replace(" ", "").lower() #Ensures that spacing and capitalization is standardized

        # User already has an account
        if user == "yes":
            users = load_users()   # Load existing users from CSV

            while True:            # Inner loop for login attempts
                userId = input("What is your user ID?: ").strip()
                password = input("What is your password?: ").strip()

                # Check if userId exists in the loaded users
                if userId in users:
                    hash_pw = users[userId]   # Stored hashed password

                    # Compare entered password with stored hash
                    if bcrypt.checkpw(password.encode("utf-8"), hash_pw.encode("utf-8")):
                        print("Login successful!")
                        return userId         # Exit and return userId on success
                    else:
                        print("Incorrect password. Try again.\n")
                else:
                    print("User ID not found. Try again.\n")

        # User does not have an account → sign them up
        elif user == "no":
            sign_up()   # Create a new account

        # If input was not yes/no
        else:
            print("Please enter a valid option!\n")

##Look Up Products

def lookup_products(products):
    """Alp Jashanica: This function takes a string and splits it up and compares it to the products.csv file if a word in the string matched it would make take the name and price as a list. It makes 2d list for all the name and prices. The parameters is a string with the names of the products. Returns the 2d list with the names(string) and prices(float).

"""
    filename = "products.csv"

    product_list = products.split(' ') # Spliting the names

    product_list_found = [] # What im returning name, price in list
    product_holder = [] # What ends up not in here means its not in file


    file = open(filename, "r") # Reading the text



    for line in file: # Checking every line

        words = line.split(",") # Its in a csv file so it seperated by commas not spaces

        if len(words) >= 2: # Making sure its a list with name and price


            product_name = words[0] # Names
            product_price = words[1] # prices

            i = 0


            while i < len(product_list):# Checking all the products given


                if product_name == product_list[i]:


                    price_str = "" # This is used to remove the /n at the end

                    j = 0


                    while j < len(product_price) - 1:


                        if j < len(product_price):

                            price_str = price_str + product_price[j] # Copied the list without the last character

                        j = j + 1

                    price = float(price_str)

                    product_list_found.append([product_name, price]) # Making the list returned

                    product_holder.append(product_name) #list of all the names that found to compare to later

                i = i + 1

    file.close()


    for name in product_list:


        if name not in product_holder:# The items in the str if not found when compared to the product_holder

            print(f"Warning message, Product {name} isn't found in file")


    return product_list_found # 2d list with name and price


##Complete Order
def complete_order(userid, product_list):
    """Kavya Sachdeva: This function calculates the total, applies a random discount, calculates tax and outputs the completed order in a order.csv file. It also prints a formatted reciepts and also prints the numer of order made till far."""
    print("\n----------- RECEIPT ------------")

    # 1. Subtotal
    subtotal = 0
    for name, price in product_list:
        print(f"{name} : ${price:.2f}")
        subtotal += price

    # 2. Discount
    discount_percent = random.randint(5, 50)
    discount_amount = subtotal * (discount_percent / 100)
    after_discount = subtotal - discount_amount

    # 3. Tax = 13%
    tax = after_discount * 0.13

    # 4. Final total
    total = after_discount + tax

    TITLE   = "\033[35m"
    LABEL   = "\033[36m"
    VALUE   = "\033[30m"
    RESET   = "\033[0m"

    print(f"{TITLE}──────  ORDER RECEIPT  ──────{RESET}")
    print()
    print(f"{LABEL}Subtotal:{RESET}        {VALUE}${subtotal:.2f}{RESET}")
    print(f"{LABEL}Discount ({discount_percent}%):{RESET} -{VALUE}${discount_amount:.2f}{RESET}")
    print(f"{LABEL}Tax (13%):{RESET}       {VALUE}${tax:.2f}{RESET}")
    print("──────────────────────────────────")
    print(f"{LABEL}TOTAL:{RESET}           {TITLE}${total:.2f}{RESET}")
    print("──────────────────────────────────")
    print()


    # 5. Write order to orders.csv (file will be created automatically)
    with open("orders.csv", "a", newline="") as f:
        writer = csv.writer(f)
        row = [userid, total] + [item[0] for item in product_list]
        writer.writerow(row)

    # 6. Count number of orders for this user
    count = 0
    with open("orders.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == userid:
                count += 1

    print(f"You have made {count} orders so far.\n")

##Customer Summary

def customer_summary(userid):
    """Madeline Berardi: This function creates a formatted summary of all orders made by a user. This includes their userid, total cost, and a list of all products they ordered and their quantities. It reads the orders.csv file for the information."""
    user_orders = []
    with open("orders.csv") as file:
        for line in file:
            order = line.strip().split(",") #Create list with only the users orders, prices, and items
            if order[0] == userid:
                order[1] = float(order[1])
                user_orders.append(order)


    order_count = 0
    total_spent = 0
    product_count = [["Sponge", 0],["Bottle", 0],["Rook", 0],["D12", 0],["Bowl", 0],["WitchHat", 0]]
    for order in user_orders:
        order_count += 1
        total_spent += order[1]
        i = 2
        while i < len(order): #Go through list to tally products
            for product in product_count:
                if product[0] == order[i]:
                    product[1] += 1 #Add a tally to each individual product ordered
            i += 1

    total_formatted = f"${total_spent:.2f}" #Variable to allow the $ to move with numbers

    print("================================")
    print("--------------------------------")
    print(f"Order summary for: \033[2;35m{userid}")
    print("\033[2;37m--------------------------------")
    print("================================\n")
    print(f"\033[2;34;1mTotal orders: \033[2;33m{order_count:>15}\n") #Formatting using colours
    print(f"\033[2;34;1mTotal spent:  \033[2;33m{total_formatted:>15}\n")
    print("\033[2;37m================================")
    print("--------------------------------")
    print(f"         Items Purchased")
    print("\033[2;37m--------------------------------")
    print("================================\n")

    for product in product_count: #Prints items only if they were purchased
        if product[1] != 0:
            left_formatted = f"\033[2;34;1m{product[0]} orders:"
            print(f"{left_formatted:<20}\033[2;33m{product[1]:>15}\033[2;37m")

##Pack Products

def pack_products(product_list):
    """This function controls the Q-arm movement to pick up each product and place it in the drop off point. It has the parameter of the product_list and returns nothing."""

    sponge_position = [0.6608102456432673, 0.1999529942109691, 0.22823204276595388]
    bottle_position = [0.6796706392833769, 0.11635265299106361, 0.23458412260927958]
    rook_position = [0.6922350414448839, 0.04413825489363385, 0.19743462250633123]
    dice_position = [0.6948418796978071, -0.026132603133685622, 0.1707916105972997]
    witchhat_position = [0.6879718495151552, -0.10153691414584821, 0.168657692721773]
    bowl_position = [0.6796268632156689, -0.18084868391010173, 0.18071288371274247]
    basket_position = [0.2767673547194245, -0.33061039331546505, 0.46930426610654363]

    x_adjust = 0 # (+) = away from arm, (-) = towards arm
    y_adjust = 0 # (+) = left, (-) = right
    z_adjust = 0.1 # (+) = up, (-) = down

    current_item = "" #Empty string to print what product is packed
    current_position = [0, 0, 0] #Empty position to allow for adjustments
    arm.home()
    for product in product_list:
        product_name = product[0]
        if product_name == "Sponge":
            current_position = sponge_position #Set variable to item position
            current_item = "Sponge"
        elif product_name == "Bottle":
            current_position = bottle_position
            current_item = "Bottle"
        elif product_name == "Rook":
            current_position = rook_position
            current_item = "Rook"
        elif product_name == "D12":
            current_position = dice_position
            current_item = "D12"
        elif product_name == "WitchHat":
            current_position = witchhat_position
            current_item = "WitchHat"
        elif product_name == "Bowl":
            current_position = bowl_position
            current_item = "Bowl"

        current_position[0] += x_adjust #Adjust these values depending on live set up
        current_position[1] += y_adjust
        current_position[2] += z_adjust

        sleep(1)
        arm.rotate_gripper(180) #Open claw (Ensure claw starts closed before running program)
        sleep(1)
        arm.set_arm_position([current_position[0], current_position[1], 0.48823204276595388]) #Move to a height above the item to not knock over other items
        sleep(1)
        arm.set_arm_position(current_position) #Lower onto item
        sleep(1)
        arm.rotate_gripper(-180) #Close claw
        sleep(1)
        arm.set_arm_position([current_position[0], current_position[1], 0.48823204276595388]) #Move up before moving to basket to not knock over items
        sleep(1)
        arm.set_arm_position(basket_position)
        sleep(1)
        arm.rotate_gripper(180)

        print(f"{current_item} packed.")

        sleep(1)
        arm.home()
        sleep(1)
        arm.rotate_gripper(-180)

## Main

def main():
    """This function executes the entire warehouse ordering system. It calls all other functions to run the program. It takes no parameters and returns nothing."""

    print("Welcome")
    userId = authenticate() #Create userid for function parameters
    condition = True
    while condition: #While loop to allow users to make multiple orders
        userDecision = input("Would you like to make a purchase?(Yes/No): ").lower()
        if userDecision == "yes":
            userProducts = lookup_products(scan_barcode())
            pack_products(userProducts)

        else:
            condition = False

    complete_order(userId,userProducts)
    customer_summary(userId)


##Call Functions
main()