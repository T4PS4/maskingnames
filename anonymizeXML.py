def ask_to_mask():

    while True:
        user_input = input("mask y/n/enter for no : ")
        if user_input.lower() == "":
            return False
        elif user_input.lower() == "y":
            return True
        elif user_input.lower() == "n":
            return False
        else:
            print("Invalid input. Please enter either 'yes' or 'no'.")

            