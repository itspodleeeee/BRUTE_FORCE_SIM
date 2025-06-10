"""
Utility functions for the Brute-Force Login Simulator.
"""
import hashlib
import random
import time
from datetime import datetime
import matplotlib.pyplot as plt
from config import *

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_captcha() -> tuple:
    """Generate a simple math CAPTCHA."""
    num1 = random.randint(CAPTCHA_MIN_NUMBER, CAPTCHA_MAX_NUMBER)
    num2 = random.randint(CAPTCHA_MIN_NUMBER, CAPTCHA_MAX_NUMBER)
    operation = random.choice(['+', '-', '*'])
    
    if operation == '+':
        answer = num1 + num2
    elif operation == '-':
        answer = num1 - num2
    else:
        answer = num1 * num2
    
    question = f"{num1} {operation} {num2}"
    return question, answer

def log_event(message: str, event_type: str = "INFO"):
    """Log an event with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{event_type}] {message}")

def plot_attack_progress(attempts_data: list, rate_limits: list, lockouts: list):
    """Plot the brute force attack progress."""
    plt.figure(figsize=(12, 6))
    
    # Plot attempts
    times, attempts = zip(*attempts_data)
    plt.plot(times, attempts, 'b-', label='Login Attempts')
    
    # Plot rate limits
    if rate_limits:
        rate_times, rate_attempts = zip(*rate_limits)
        plt.scatter(rate_times, rate_attempts, color='red', label='Rate Limited')
    
    # Plot lockouts
    if lockouts:
        lockout_times, lockout_attempts = zip(*lockouts)
        plt.scatter(lockout_times, lockout_attempts, color='black', label='Account Locked')
    
    plt.title('Brute Force Attack Progress')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Attempt Number')
    plt.legend()
    plt.grid(True)
    plt.show()

def create_default_users():
    """Create default users if users.json doesn't exist."""
    import json
    import os
    
    if not os.path.exists(USERS_FILE):
        default_users = {
            "admin": {
                "password": hash_password("admin123"),
                "failed_attempts": 0,
                "last_attempt": 0,
                "locked_until": 0
            },
            "user1": {
                "password": hash_password("password123"),
                "failed_attempts": 0,
                "last_attempt": 0,
                "locked_until": 0
            }
        }
        
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=4)

def create_password_list():
    """Create a default password list if it doesn't exist."""
    import os
    
    if not os.path.exists(PASSWORD_LIST_FILE):
        common_passwords = [
            "password123",
            "admin123",
            "123456",
            "qwerty",
            "letmein",
            "welcome",
            "monkey123",
            "dragon",
            "baseball",
            "football",
            "superman",
            "trustno1",
            "iloveyou",
            "sunshine",
            "master",
            "hello123",
            "shadow",
            "ashley",
            "michael",
            "hunter"
        ]
        
        with open(PASSWORD_LIST_FILE, 'w') as f:
            f.write('\n'.join(common_passwords)) 