def about():
    print("\nMatdarMitra helps voters choose the correct ECI form.")
    print("It provides information about voter registration.")

def sample_questions():
    print("\nSample Questions:")
    print("1. What documents are needed for Form 6?")
    print("2. Which form is used for name correction?")
    print("3. Who can object to a voter registration?")
    print("4. Which form is used after shifting residence?")

def check_form():
    print("\nSelect your requirement:")
    print("1. New voter registration")
    print("2. Shifting residence")
    print("3. Name correction")
    print("4. Remove name from voter list")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("You need Form 6.")
    elif choice == "2":
        print("You need Form 8.")
    elif choice == "3":
        print("You need Form 8.")
    elif choice == "4":
        print("You need Form 7.")
    else:
        print("Invalid choice!")
while True:
    print("\n===== MATDARMITRA MENU =====")
    print("1. About MatdarMitra")
    print("2. Sample Questions")
    print("3. Check ECI Form")
    print("0. Exit")

    option = input("Enter your option: ")

    if option == "1":
        about()

    elif option == "2":
        sample_questions()

    elif option == "3":
        check_form()

    elif option == "0":
        print("Thank you for using MatdarMitra!")
        break

    else:
        print("Invalid option! Please try again.")
