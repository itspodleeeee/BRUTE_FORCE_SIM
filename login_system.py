"""
My login system with some cool security stuff
Made for my security class project
"""
import json
import time
from typing import Tuple, Optional
from config import *
from utils import hash_password, generate_captcha, log_event

class LoginSystem:
    def __init__(self):
        # Load up our users and set up some tracking stuff
        self.load_users()
        self.attempt_count = 0  # Keep track of how many times people try to log in
        self.lockout_count = {}  # Remember how many times each user got locked out
        self.user_attempts = {}  # Count attempts for each user
        self.captcha_required = {}  # Track who needs to solve a CAPTCHA
        self.user_lockouts = {}  # Keep track of lockouts for users that don't exist yet
    
    def load_users(self):
        """Load our users from the JSON file"""
        try:
            with open(USERS_FILE, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}
    
    def save_users(self):
        """Save our users back to the JSON file"""
        with open(USERS_FILE, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def check_rate_limit(self, username: str) -> bool:
        """Check if someone is trying too many times too fast"""
        if username not in self.users:
            return False
        
        current_time = time.time()
        user = self.users[username]
        
        # Reset the counter if it's been long enough
        if current_time - user['last_attempt'] > RATE_LIMIT_WINDOW:
            user['failed_attempts'] = 0
            user['last_attempt'] = current_time
            return False
        
        return user['failed_attempts'] >= RATE_LIMIT_ATTEMPTS
    
    def check_account_lockout(self, username: str) -> Tuple[bool, Optional[int]]:
        """Check if an account is locked and how long they have to wait"""
        current_time = time.time()
        
        # Check if a non-existent user is locked out
        if username not in self.users:
            if username in self.user_lockouts and self.user_lockouts[username] > current_time:
                remaining_time = int(self.user_lockouts[username] - current_time)
                return True, remaining_time
            return False, None
        
        # Check if a real user is locked out
        user = self.users[username]
        if user['locked_until'] > current_time:
            remaining_time = int(user['locked_until'] - current_time)
            return True, remaining_time
        
        return False, None
    
    def calculate_lockout_time(self, username: str) -> int:
        """Figure out how long to lock someone out (gets longer each time)"""
        if username not in self.lockout_count:
            self.lockout_count[username] = 0
        
        lockout_time = INITIAL_LOCKOUT_TIME + (self.lockout_count[username] * LOCKOUT_TIME_INCREMENT)
        self.lockout_count[username] += 1
        return lockout_time
    
    def should_show_captcha(self, username: str) -> bool:
        """Check if we should make them solve a CAPTCHA"""
        if username not in self.user_attempts:
            self.user_attempts[username] = 0
            self.captcha_required[username] = False
        
        self.user_attempts[username] += 1
        if self.user_attempts[username] % 3 == 0:  # Show CAPTCHA every 3rd try
            self.captcha_required[username] = True
            return True
        return False
    
    def is_captcha_required(self, username: str) -> bool:
        """Check if they still need to solve a CAPTCHA"""
        return self.captcha_required.get(username, False)
    
    def verify_login(self, username: str, password: str) -> Tuple[bool, str]:
        """Check if their login is good and handle all the security stuff"""
        # First check if they need to solve a CAPTCHA
        if self.is_captcha_required(username):
            return False, "CAPTCHA required before next attempt"
        
        current_time = time.time()
        
        # Check if they're locked out first
        is_locked, remaining_time = self.check_account_lockout(username)
        if is_locked:
            log_event(f"Account locked for {username}. {remaining_time}s remaining", "WARNING")
            return False, f"You cannot attempt again for {remaining_time} seconds"
        
        # Check if the user exists
        if username not in self.users:
            log_event(f"Login attempt for non-existent user: {username}", "WARNING")
            self.attempt_count += 1
            
            # Keep track of attempts for non-existent users too
            if username not in self.user_attempts:
                self.user_attempts[username] = 0
            self.user_attempts[username] += 1
            
            # Lock them out if they try too many times
            if self.user_attempts[username] >= MAX_LOGIN_ATTEMPTS:
                lockout_time = self.calculate_lockout_time(username)
                self.user_lockouts[username] = current_time + lockout_time
                return False, f"You cannot attempt again for {lockout_time} seconds"
            
            return False, "Invalid username or password"
        
        user = self.users[username]
        
        # Check if they're trying too fast
        if self.check_rate_limit(username):
            log_event(f"Rate limit exceeded for {username}", "WARNING")
            return False, "Too many attempts. Please wait before trying again"
        
        # Check if the password is right
        if user['password'] == hash_password(password):
            # Reset their failed attempts if they get it right
            user['failed_attempts'] = 0
            user['last_attempt'] = current_time
            self.save_users()
            log_event(f"Successful login for {username}", "INFO")
            return True, "Login successful"
        
        # Handle wrong password
        user['failed_attempts'] += 1
        self.attempt_count += 1
        user['last_attempt'] = current_time
        
        # Lock them out if they fail too many times
        if user['failed_attempts'] >= MAX_LOGIN_ATTEMPTS:
            lockout_time = self.calculate_lockout_time(username)
            user['locked_until'] = current_time + lockout_time
            log_event(f"Account locked for {username} due to too many failed attempts", "WARNING")
            self.save_users()
            return False, f"You cannot attempt again for {lockout_time} seconds"
        
        self.save_users()
        log_event(f"Failed login attempt for {username}", "WARNING")
        return False, "Invalid username or password"
    
    def solve_captcha(self, username: str) -> bool:
        """Make them solve a math problem to prove they're human"""
        while True:
            question, answer = generate_captcha()
            print(f"\nCAPTCHA: Solve this math problem: {question}")
            try:
                user_answer = int(input("Your answer: "))
                if user_answer == answer:
                    print("CAPTCHA solved successfully!")
                    self.captcha_required[username] = False  # They solved it, no more CAPTCHA needed
                    return True
                else:
                    print("Incorrect answer. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def get_attempt_count(self) -> int:
        """Get how many times people have tried to log in"""
        return self.attempt_count
    
    def wait_for_lockout(self, username: str):
        """Wait for the lockout to end and make them solve a CAPTCHA"""
        while True:
            is_locked, remaining_time = self.check_account_lockout(username)
            if not is_locked:
                break
            print(f"\rWaiting... {remaining_time} seconds remaining", end="", flush=True)
            time.sleep(1)
        print("\nLockout period ended. Solve CAPTCHA and you can try again.")
        self.captcha_required[username] = True  # Make them solve a CAPTCHA after lockout
        self.solve_captcha(username)  # Show the CAPTCHA right away 