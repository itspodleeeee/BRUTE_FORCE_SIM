"""
Configuration settings for the Brute-Force Login Simulator.
"""

# Login system settings
MAX_LOGIN_ATTEMPTS = 3
INITIAL_LOCKOUT_TIME = 30  # seconds for first lockout
LOCKOUT_TIME_INCREMENT = 60  # additional seconds for each subsequent lockout
RATE_LIMIT_ATTEMPTS = 5
RATE_LIMIT_WINDOW = 60  # seconds

# CAPTCHA settings
CAPTCHA_TRIGGER_AFTER = 3  # Show CAPTCHA after this many failed attempts
CAPTCHA_MIN_NUMBER = 1
CAPTCHA_MAX_NUMBER = 10

# File paths
USERS_FILE = "users.json"
PASSWORD_LIST_FILE = "password_list.txt"

# Attack simulation settings
ATTACK_DELAY = 0.5  # seconds between attempts 