def project_card(product, user, problem, data_source):
    print("\n===== PROJECT CARD =====")
    print(f"Product     : {product}")
    print(f"User        : {user}")
    print(f"Problem     : {problem}")
    print(f"Data Source : {data_source}")


# Function arguments
project_card(
    "MatdarMitra",
    "First-time and shifting voters",
    "Confusion about voter registration forms and documents",
    "Election Commission of India (ECI)"
)

# User input
name = input("\nEnter your name: ")
question = input("Enter your question: ")

print(f"\nHello {name}!")
print(f"Your question: {question}")
print("Welcome to MatdarMitra!")
