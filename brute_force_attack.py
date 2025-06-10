"""
My brute force attack simulator
Made for my security class project
"""
import time
from typing import List, Tuple
from config import *
from login_system import LoginSystem
from utils import log_event, plot_attack_progress

class BruteForceAttack:
    def __init__(self, login_system: LoginSystem):
        self.login_system = login_system
        self.attempts_data = []  # Keep track of when we tried each password
        self.rate_limits = []    # Remember when we hit rate limits
        self.lockouts = []       # Remember when we got locked out
        self.start_time = 0
        self.attempt_count = 0
    
    def load_password_list(self) -> List[str]:
        """Load up our list of passwords to try"""
        try:
            with open(PASSWORD_LIST_FILE, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            log_event("Password list file not found!", "ERROR")
            return []
    
    def handle_lockout(self, target_username: str, lockout_time: int):
        """Wait out the lockout and make them solve a CAPTCHA"""
        print(f"\nAccount locked for {lockout_time} seconds")
        print("Waiting for lockout period to end...")
        
        # Show a countdown
        for remaining in range(lockout_time, 0, -1):
            print(f"\rTime remaining: {remaining} seconds", end="", flush=True)
            time.sleep(1)
        print("\nLockout period ended. Solve CAPTCHA to continue.")
        
        # Make them solve a CAPTCHA after waiting
        if not self.login_system.solve_captcha(target_username):
            print("CAPTCHA failed - skipping attempt")
            return False
        return True
    
    def simulate_attack(self, target_username: str):
        """Try to break into an account by trying lots of passwords"""
        passwords = self.load_password_list()
        if not passwords:
            log_event("No passwords to try!", "ERROR")
            return
        
        self.start_time = time.time()
        self.attempt_count = 0
        self.attempts_data = []
        self.rate_limits = []
        self.lockouts = []
        
        log_event(f"Starting brute force attack on user: {target_username}", "ATTACK")
        print("\nAttack Progress:")
        print("-" * 50)
        
        for password in passwords:
            # Check if we're locked out
            is_locked, remaining_time = self.login_system.check_account_lockout(target_username)
            if is_locked:
                print(f"\nAccount is currently locked. {remaining_time} seconds remaining.")
                if not self.handle_lockout(target_username, remaining_time):
                    continue
            
            # Check if we need to solve a CAPTCHA
            if self.login_system.is_captcha_required(target_username):
                print("\nCAPTCHA required before next attempt!")
                if not self.login_system.solve_captcha(target_username):
                    print("CAPTCHA failed - skipping attempt")
                    continue
            
            self.attempt_count += 1
            current_time = time.time() - self.start_time
            
            # Remember this attempt
            self.attempts_data.append((current_time, self.attempt_count))
            
            # Try to log in
            success, message = self.login_system.verify_login(target_username, password)
            
            # Show what happened
            print(f"\nAttempt {self.attempt_count}:")
            print(f"Trying password: {password}")
            print(f"Result: {message}")
            
            # Handle rate limiting
            if "Too many attempts" in message:
                self.rate_limits.append((current_time, self.attempt_count))
                print("Rate limit triggered - waiting...")
                time.sleep(RATE_LIMIT_WINDOW)
                continue  # Skip to next attempt after rate limit
            
            # Handle getting locked out
            if "You cannot attempt again for" in message:
                self.lockouts.append((current_time, self.attempt_count))
                try:
                    lockout_time = int(message.split()[-2])
                    if not self.handle_lockout(target_username, lockout_time):
                        continue
                except (ValueError, IndexError):
                    print("Error parsing lockout time")
                    continue
            
            # Check if we need to solve a CAPTCHA after failing
            if not success and self.login_system.should_show_captcha(target_username):
                print("\nCAPTCHA triggered!")
                if not self.login_system.solve_captcha(target_username):
                    print("CAPTCHA failed - skipping attempt")
                    continue
            
            # If we got in, we're done!
            if success:
                log_event(f"Attack successful! Password found: {password}", "SUCCESS")
                break
            
            # Wait a bit between tries
            time.sleep(ATTACK_DELAY)
        
        # Show how the attack went
        self.plot_results()
    
    def plot_results(self):
        """Make a cool graph of our attack"""
        if self.attempts_data:
            plot_attack_progress(self.attempts_data, self.rate_limits, self.lockouts) 