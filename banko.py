import uuid

class Account:
    def __init__(self, name, email, address, account_type):
        self.account_number = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.transaction_history = []
        self.loan_count = 0

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited: {amount}")
        return f"{amount} deposited successfully."

    def withdraw(self, amount):
        if amount > self.balance:
            return "Withdrawal amount exceeded"
        self.balance -= amount
        self.transaction_history.append(f"Withdrew: {amount}")
        return f"{amount} withdrawn successfully."

    def check_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if self.loan_count >= 2:
            return "Loan limit reached"
        self.balance += amount
        self.loan_count += 1
        self.transaction_history.append(f"Loan taken: {amount}")
        return f"Loan of {amount} taken successfully."

    def transfer(self, amount, recipient_account):
        if amount > self.balance:
            return "Insufficient funds"
        if not recipient_account:
            return "Account does not exist"
        self.balance -= amount
        recipient_account.balance += amount
        self.transaction_history.append(f"Transferred: {amount} to {recipient_account.account_number}")
        recipient_account.transaction_history.append(f"Received: {amount} from {self.account_number}")
        return f"{amount} transferred successfully."

class Bank:
    def __init__(self):
        self.accounts = {}
        self.total_balance = 0
        self.total_loan_amount = 0
        self.loan_enabled = True

    def create_account(self, name, email, address, account_type):
        account = Account(name, email, address, account_type)
        self.accounts[account.account_number] = account
        return account

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return f"Account {account_number} deleted successfully."
        return "Account does not exist"

    def get_all_accounts(self):
        return self.accounts.keys()

    def check_total_balance(self):
        return sum(account.balance for account in self.accounts.values())

    def check_total_loan_amount(self):
        return sum(account.loan_count * account.balance for account in self.accounts.values())

    def toggle_loan_feature(self, status):
        self.loan_enabled = status
        return f"Loan feature set to {status}"

    def find_account(self, name, address):
        for account in self.accounts.values():
            if account.name == name and account.address == address:
                return account
        return None

class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, name, email, address, account_type):
        return self.bank.create_account(name, email, address, account_type)

    def delete_account(self, account_number):
        return self.bank.delete_account(account_number)

    def get_all_accounts(self):
        return self.bank.get_all_accounts()

    def check_total_balance(self):
        return self.bank.check_total_balance()

    def check_total_loan_amount(self):
        return self.bank.check_total_loan_amount()

    def toggle_loan_feature(self, status):
        return self.bank.toggle_loan_feature(status)

def user_menu(user):
    while True:
        print("\nUser Menu:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Take Loan")
        print("6. Transfer")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter deposit amount: "))
            print(user.deposit(amount))
        elif choice == "2":
            amount = float(input("Enter withdrawal amount: "))
            print(user.withdraw(amount))
        elif choice == "3":
            print("Current Balance:", user.check_balance())
        elif choice == "4":
            print("Transaction History:")
            for transaction in user.get_transaction_history():
                print(transaction)
        elif choice == "5":
            amount = float(input("Enter loan amount: "))
            if admin.bank.loan_enabled:
                print(user.take_loan(amount))
            else:
                print("Loan feature is currently disabled")
        elif choice == "6":
            recipient_account_number = input("Enter recipient account number: ")
            recipient_account = admin.bank.accounts.get(recipient_account_number)
            amount = float(input("Enter transfer amount: "))
            print(user.transfer(amount, recipient_account))
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

def user_system(admin):
    print("Welcome to the User System!")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    address = input("Enter your address: ")
    account_type = input("Enter your account type (Savings/Current): ")

    user = admin.create_account(name, email, address, account_type)

    print(f"Account created successfully! Your account number is: {user.account_number}")

    user_menu(user)

def user_login(admin):
    print("User Login")
    name = input("Enter your name: ")
    address = input("Enter your address: ")

    user = admin.bank.find_account(name, address)
    if user:
        print(f"Login successful! Your account number is: {user.account_number}")
        user_menu(user)
    else:
        print("Account not found. Please check your name and address.")

def admin_system(admin):
    print("Welcome to the Admin System!")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == "admin" and password == "admin":
        print("Admin login successful!")

        while True:
            print("\nAdmin Menu:")
            print("1. Create Account")
            print("2. Delete Account")
            print("3. List All Accounts")
            print("4. Check Total Balance")
            print("5. Check Total Loan Amount")
            print("6. Toggle Loan Feature")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter user's name: ")
                email = input("Enter user's email: ")
                address = input("Enter user's address: ")
                account_type = input("Enter user's account type (Savings/Current): ")
                user = admin.create_account(name, email, address, account_type)
                print(f"Account created successfully! Account Number: {user.account_number}")
            elif choice == "2":
                account_number = input("Enter account number to delete: ")
                print(admin.delete_account(account_number))
            elif choice == "3":
                print("List of all accounts:")
                for account_number in admin.get_all_accounts():
                    user = admin.bank.accounts[account_number]
                    print(f"Name: {user.name}, Account Number: {user.account_number}")
            elif choice == "4":
                print("Total Balance:", admin.check_total_balance())
            elif choice == "5":
                print("Total Loan Amount:", admin.check_total_loan_amount())
            elif choice == "6":
                status = input("Enter loan feature status (True/False): ")
                print(admin.toggle_loan_feature(status == 'True'))
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid username or password.")

if __name__ == "__main__":
    bank = Bank()
    admin = Admin(bank)

    print("Welcome to the Banking Management System!")

    while True:
        print("Main Menu:")
        print("1. User System")
        print("2. User Login")
        print("3. Admin System")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_system(admin)
        elif choice == "2":
            user_login(admin)
        elif choice == "3":
            admin_system(admin)
        elif choice == "4":
            print("Thank you for using the Banking Management System!")
            break
        else:
            print("Invalid choice. Please try again.")
