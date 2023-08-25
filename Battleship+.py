# List of import
import pickle
from datetime import date
from string import punctuation
from Battleship_game_module import game
import os
#Main Menu Variable
dob_len = 8
minimum_password_length = 8
login_attempts = 3
user_database = ""
game_status = True

### MAIN MENU CORE ###

# Functionality: Binary search function for integer in list
# In Battleship+, it is used for quick check for user input against
# a list of valid months.
# Parameters:
#	key: element in the list of months
#	search: user’s input (corresponding month’s number)
# Returns:
#	True if user-inputted month is found in the list of months
#       (aka valid month)
#	False if user-inputted month is not found in the list
# Author: Jackson and Haoyang
def binary_search(key,search):
    low = 0
    high = len(search) - 1
    while low <= high:
        mid = (low+high)//2
        if search[mid] == key:
            return True
        elif search[mid] > key:
            high = mid -1
        else:
            low = mid + 1
    return False

# Functionality: Load file containing user information
# Parameters: file_name: name of the file
# Returns: account: the file containing dictionary of user information
# Author: Jackson
def load_file(file_name):
    try:
        with open('database.pickle', 'rb') as file_name:
            account = pickle.load(file_name)
            return account
    except FileNotFoundError: # creates a new dictionary if none found (but users don't need to know that)
        print("User information cannot be retrieved at the moment. System will retrieve it when available.")
        account = {}
        return account

# Functionality: Save file containing user information
# so that information will not be lost when program ends
# Parameters:
#	file: dictionary of user information
#	file_name: name of the file
# Author: Jackson
def save_file(file,file_name):
  with open('database.pickle', 'wb') as file_name:
      pickle.dump(file, file_name)

# Functionality to check if password meets requirements
# (min. length, at least one uppercase letter, lowercase letter and digit,
# at least one special symbol)
# Parameters: password_data: User’s password
# Returns: True if password meets all requirements, else False
# Author: Joel and Haoyang
def password(password_data,username_data):
    total_conditions_met = 0
    at_least_one_digit = False
    at_least_one_lowercase_letter = False
    at_least_one_uppercase_letter = False
    at_least_one_special_symbol = False
    for c in password_data:
        if c.isdigit():
            at_least_one_digit = True
        elif c.islower():
            at_least_one_lowercase_letter = True
        elif c.isupper():
            at_least_one_uppercase_letter = True
        elif c in punctuation:
            at_least_one_special_symbol = True
    if len(password_data)> minimum_password_length: # password must be greater than 8 characters
        total_conditions_met += 1
    else:
        print("Password must be more than {} characters long.".format(minimum_password_length))
    if password_data == "":
        print("Password cannot be empty.")
    else:
        total_conditions_met +=1
    if username_data in password_data:
        print("Password cannot contain username.")
    else:
        total_conditions_met +=1
    if at_least_one_digit:
        total_conditions_met += 1
    else:
        print("Password must contain at least 1 digit")
    if at_least_one_lowercase_letter:
        total_conditions_met += 1
    else:
        print("Password must contain at least 1 lowercase letter.")
    if at_least_one_uppercase_letter:
        total_conditions_met += 1
    else:
        print("Password must contain at least 1 uppercase letter.")
    if at_least_one_special_symbol:
        total_conditions_met += 1
    else:
        print("Password must contain at least 1 special character.")
    if total_conditions_met == 7:
        return True
    else:
        return False

# Functionality: Checks if user inputs a valid date of birth (DOB)
# Parameters: dob_data: User’s date of birth
# Returns: True if valid DOB, else False
# Author: Jackson and Joel
def dob(dob_data):
    month_31 = ("01","03","05","07","08","10","12")
    month_30 = ("04","06","09","11")
    #Check if DOB has 8 numbers
    if len(dob_data) != dob_len:
        print("Enter your DOB as DDMMYYYY: ")
        return False
    elif not dob_data.isdigit():
        print("Enter your DOB in numbers")
        return False
    #Check if the day and month is valid
    if dob_data[0:2] == "00":
        print("Please enter a valid date")
        return False
    elif dob_data[2:4] == "00":
        print("Please enter a valid month")
        return False
    elif binary_search(dob_data[2:4],month_31):
        if int(dob_data[0:2]) > 31:
            print("There are 31 days in that month.")
            return False
    elif binary_search(dob_data[2:4],month_30):
        if int(dob_data[0:2]) > 30:
            print("There are 30 days in that month.")
            return False
    elif dob_data[2:4] == "02" and int(dob_data[4:])%4 == 0 and int(dob_data[4:])%400 == 0:
        if int(dob_data[0:2]) > 29:
            print("There were 29 days in February that year.")
            return False
    elif dob_data[2:4] == "02":
        if int(dob_data[0:2]) > 28:
            print("There are 28 days in February.")
            return False
    else:
        print("There are 12 months in a year.")
        return False
    #Check if the birth year is within expected norm
    if int(dob_data[4:]) >= date.today().year or int(dob_data[4:]) <= date.today().year - 100:
        print("Invalid birth year.")
        return False
    else:
        return True

# Functionality: Create a new account
# Account info will be saved in a file if valid
# (password and birthdate requirements met). Otherwise, it will
# repeatedly prompt user for valid account info
# Author: Jackson and Joel
def create_account():
   valid_username = False
   valid_password = False
   valid_dob = False
   print("--------------CREATE ACCOUNT--------------")
   user_account = load_file(user_database)
   while not valid_username:
       username_data = input("Username (Enter '#' to return to main menu): ")
       if not username_data in user_account:
           if username_data == '':
               print("username cannot be empty.")               
           else:
               hashtag = False
               space = False
               for i in username_data:
                   if i.isspace():
                       print("There cannot be empty space in username.")
                       space = True
                       break
                   if i == '#':
                       print('There cannot be # in username')
                       hashtag = True
                       break
               if not space and not hashtag:
                   valid_username = True
       else:
           print("Username has been used, please try another.")
   if not valid_password: 
   # enter valid password, check based on password function
       print("Password must meet the following conditions: \n\
    1. More than {} characters\n\
    2. Contain at least one upper and lower case\n\
    3. Contain at least one digit\n\
    4. Contain at least one special characters".format(minimum_password_length))
   while not valid_password:
       password_data = input("Choose a password: ")
       if username_data in password_data:
           print("Password cannot contain username, please try again!")
       elif password(password_data,username_data):
           valid_password = True

   # enter valid dob, check based on dob function
   while not valid_dob:
       dob_data = input("Enter your Date of Birth (DDMMYYYY): ")
       if dob(dob_data):
           valid_dob = True
   user_account.update({username_data: [dob_data, 0, password_data, 0]})
   # user_account[username][1] is the counter to check if account is locked
   # 0 means unlocked, 1 means locked
   # user_account[username][3] is the number of login attempts (initially 0)    
   save_file(user_account, user_database)
   print("Account has been created!")
   print("Returning to main menu...")

# Functionality: Reset locked accounts
# Users can unlock their account and reset their password
# by entering the correct birthday. 
# Author: Jackson and Joel
def recover_account():
  user_reset = False
  print("----------------RECOVER ACCOUNT----------------")
  user_account = load_file(user_database)
  username_data = ""
  while username_data != "#":
      username_data = input("Enter Username (Enter '#' to return to main menu): ")
      if username_data == "#":
          break # exit loop early and go directly to main menu
      recover_dob = input("Enter DOB: ")
      if not user_account.get(username_data, False):
          print("Invalid Username or Date of Birth. We are unable to verify your identity and unlock your account.")
      elif user_account[username_data][0] == recover_dob:
          user_reset = True
          break
      else:
          print("Invalid Username or Date of Birth. We are unable to verify your identity and unlock your account.")


  while user_reset:
      new_password = input("Enter new password: ")
      if new_password == user_account[username_data][2]:
          print("You have entered your old password, please try again!")
      elif password(new_password,username_data):
          user_account.update({username_data: [recover_dob, 0, new_password, 0]})
          save_file(user_account, user_database)
          print("Your password has been changed!")
          user_reset = False


  print("Returning to main menu...")

# Functionality: Allow users to login with their account.
# It will grant access to actual game if login information is valid.
# If not, they will have a maximum of 3 tries before account is locked
# and they are returned to the main menu
# Author: Haoyang
def login_menu():
   global game_status
   print("-------------LOGIN-------------")
   user_account = load_file(user_database)
   username = ""
   while username != "#":
       username = input("Enter Username (Enter '#' to return to main menu): ")
       if username == "#":
           print("Returning to main menu...")
           break # exit loop early and go directly to main menu
       user_password = input("Enter Password: ")
       if not user_account.get(username, False):  # if username invalid
           print("Invalid username or password.")
       elif user_account[username][1] == 1:
           print("Your account has already been locked. Please recover it!")
           print("Returning to main menu...")
           break
       elif user_account[username][2] == user_password:
           user_account.update({username: [user_account[username][0], 0, user_account[username][2], 0]})
           # login attempts reset to 0
           save_file(user_account, user_database)
           print("{}, get ready to play Battleship+!".format(username))
           game_status = game()
           break

       else:  # if username valid but password wrong
           attempts = user_account[username][3]
           attempts += 1
           print("Invalid username or password.")
           user_account.update({username: [user_account[username][0], 0, user_account[username][2], attempts]})
           save_file(user_account, user_database)
           print("You have {} out of {} attempts left.".format(login_attempts - attempts, login_attempts))
           if user_account[username][3] == login_attempts:
               user_account.update({username: [user_account[username][0], 1, user_account[username][2], attempts]})
               save_file(user_account, user_database)
               print("Your account has been locked!")
               print("Returning to main menu...")
               break

### MAIN MENU ###

# Battleship Main Menu. Users can create account, log in, reset account or quit.
# Author: Jackson and Joel
os.system('mode con: cols=120 lines=40')
while game_status:
    print("--------MAIN MENU--------")
    print("Welcome to Battleship+!\n 1: Login\n 2: Create account\n 3: Recover Account\n 4: Quit")
    selection = input("Enter selection: ")
    if selection == "1":
        login_menu()
    elif selection == "2":
        create_account()
    elif selection == "3":
        recover_account()
    elif selection == "4":
        print("This programme was designed by Group 3 consisting of Jackson, Joel and Haoyang.")
        print("We hope you enjoyed our version of Battleship and thank you for playing.")
        break
    else:
        print("Invalid selection.")
else:
    print("This programme was designed by Group 3 consisting of Jackson, Joel and Haoyang.")
    print("We hope you enjoyed our version of Battleship and thank you for playing.")

