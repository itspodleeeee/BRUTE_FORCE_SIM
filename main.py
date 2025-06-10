"""
My brute force login simulator
Made for my security class project
"""
from login_system import LoginSystem
from brute_force_attack import BruteForceAttack
from utils import create_default_users, create_password_list, log_event
from config import CAPTCHA_TRIGGER_AFTER

def display_menu():
    """Show the main menu"""
    print("\nBrute-Force Login Simulator")
    print("=" * 30)
    print("1. Manual Login")
    print("2. Start Brute Force Attack")
    print("3. Exit")
    print("=" * 30)

def display_login_header():
    """Show the login screen header"""
    print("\nLogin Section")
    print("=" * 30)
    print("Note: To return to main menu, you need to restart the program")
    print("=" * 30)

def manual_login(login_system: LoginSystem):
    """Let someone try to log in manually"""
    display_login_header()
    
    while True:
        print(f"\nTotal login attempts: {login_system.get_attempt_count()}")
        username = input("\nEnter username (or 'q' to quit): ")
        
        if username.lower() == 'q':
            print("\nPlease restart the program to return to main menu")
            continue
        
        # Check if they need to solve a CAPTCHA first
        if login_system.is_captcha_required(username):
            print("\nCAPTCHA required to verify you're not a robot!")
            login_system.solve_captcha(username)  # Keep trying until they get it right
            continue
            
        password = input("Enter password: ")
        
        success, message = login_system.verify_login(username, password)
        print(f"\nResult: {message}")
        
        # Handle getting locked out
        if "You cannot attempt again for" in message:
            login_system.wait_for_lockout(username)  # This will show CAPTCHA after lockout
            continue

def start_attack(login_system: LoginSystem):
    """Start trying to break into an account"""
    target_username = input("\nEnter target username to attack: ")
    attacker = BruteForceAttack(login_system)
    attacker.simulate_attack(target_username)

def main():
    """The main program"""
    # Set up some default stuff
    create_default_users()
    create_password_list()
    
    # Make our login system
    login_system = LoginSystem()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            manual_login(login_system)
        elif choice == "2":
            start_attack(login_system)
        elif choice == "3":
            log_event("Program terminated", "INFO")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 