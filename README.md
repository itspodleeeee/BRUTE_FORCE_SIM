# Brute-Force Login Simulator

A Python-based simulator that demonstrates brute force attacks on login systems and the security measures used to prevent them.

## Author
**itspodleeeee**

## Features

### Security Measures
- **Rate Limiting**: Prevents too many attempts in a short time window
- **Account Lockout**: Progressive lockout periods after multiple failed attempts
- **CAPTCHA Challenges**: 
  - Triggered after every 3rd failed attempt
  - Required after lockout periods
  - Must be solved before next login attempt
- **Password Hashing**: Secure storage of passwords using SHA-256
- **Attempt Tracking**: Per-user and global attempt counting
- **Event Logging**: Detailed logging of all security events

### Attack Simulation
- **Manual Login Testing**: Test the security measures manually
- **Automated Brute Force**: Simulate automated password attacks
- **Attack Visualization**: Plot attack progress and security events
- **Customizable Password Lists**: Use your own password dictionary
- **Real-time Feedback**: See security measures in action

## Requirements
- Python 3.6+
- Required packages (install via `pip install -r requirements.txt`):
  - matplotlib
  - numpy

## Installation
1. Clone the repository:
```bash
git clone https://github.com/itspodleeeee/Brute_Force_sim.git
cd Brute_Force_sim
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Simulator
```bash
python main.py
```

### Menu Options
1. **Manual Login**: Test the login system manually
   - Enter username and password
   - Experience security measures firsthand
   - See CAPTCHA challenges and lockouts

2. **Start Brute Force Attack**: Simulate automated attacks
   - Enter target username
   - Watch security measures in action
   - View attack progress visualization

3. **Exit**: Close the program

### Security Features in Action
- **Rate Limiting**: After too many attempts in a short time
- **Account Lockout**: Progressive lockout periods
- **CAPTCHA Challenges**: 
  - After every 3rd failed attempt
  - After lockout periods
  - Must be solved correctly to continue

## Configuration
Edit `config.py` to customize:
- Rate limiting parameters
- Lockout durations
- CAPTCHA settings
- Attack simulation parameters

## File Structure
- `main.py`: Program entry point
- `login_system.py`: Core login and security logic
- `brute_force_attack.py`: Attack simulation implementation
- `utils.py`: Helper functions and utilities
- `config.py`: Configuration settings
- `users.json`: User database
- `password_list.txt`: Dictionary for brute force attacks

## Security Features Details

### Rate Limiting
- Tracks attempts within a time window
- Blocks further attempts if limit exceeded
- Window resets after timeout

### Account Lockout
- Progressive lockout periods
- Increases with each lockout
- Requires CAPTCHA after lockout

### CAPTCHA System
- Math-based challenges
- Required after every 3rd failed attempt
- Required after lockout periods
- Must be solved correctly to continue

### Password Security
- SHA-256 hashing
- Secure storage in JSON
- No plaintext passwords

## Contributing
Feel free to submit issues and enhancement requests!

## License
This project is licensed under the MIT License - see the LICENSE file for details. 