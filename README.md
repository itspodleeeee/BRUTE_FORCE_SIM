# Brute-Force Login Simulator 🔐

![Duck Signature](https://cdn-icons-png.flaticon.com/128/3975/3975090.png)

A Python-based simulator demonstrating brute force attacks on login systems and the common security measures used to prevent them.

---

## Author 👨‍💻  
**itspodleeeee**

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)  
[![Security](https://img.shields.io/badge/security-educational-yellow)](https://github.com/itspodleeeee/Brute_Force_sim)  

---

## Features 🚀

### Security Measures 🛡️
- **Rate Limiting** ⏱️: Limits rapid login attempts within a time window  
- **Account Lockout** 🔒: Progressive lockouts after multiple failed attempts  
- **CAPTCHA Challenges** 🤖:  
  - Triggered after every 3rd failed attempt  
  - Required after lockout periods  
  - Must be solved before next login attempt  
- **Password Hashing** 🔐: Passwords securely stored with SHA-256  
- **Attempt Tracking** 📊: Per-user and global login attempt monitoring  
- **Event Logging** 📝: Logs all security-related events in detail  

### Attack Simulation 💻
- **Manual Login Testing** 👆: Test login security manually  
- **Automated Brute Force** 🤖: Simulate password attack scripts  
- **Attack Visualization** 📈: Graphically display attack progress and responses  
- **Custom Password Lists** 📋: Use your own password dictionaries  
- **Real-time Feedback** ⚡: Observe security features activating live  

---

## Requirements 📋
- Python 3.6 or higher  
- Dependencies (install via `pip install -r requirements.txt`):  
  - matplotlib  
  - numpy  

---

## Installation 🛠️
```bash
git clone https://github.com/itspodleeeee/Brute_Force_sim.git
cd Brute_Force_sim
pip install -r requirements.txt
```

---

## Usage 📖

### Run the Simulator 🚀
```bash
python main.py
```

### Menu Overview 📱
1. **Manual Login** 👤  
   - Input username and password to test security  
   - Experience CAPTCHA prompts and lockouts firsthand  

2. **Start Brute Force Attack** ⚔️  
   - Specify a target username  
   - Watch the simulation and visual progress of automated attacks  

3. **Exit** 🚪  
   - Quit the application  

---

## Default Credentials 🔑

These user accounts are automatically created when the program is first run (via `create_default_users()` in `utils.py`). The passwords are securely stored as SHA-256 hashes in `users.json`.

Use these to manually test the login system:

| Username | Password    |
|----------|-------------|
| admin    | admin123    |
| user1    | password123 |

> 🛡️ These accounts are for **educational simulation only**. Always use secure credential practices in real-world applications.

---

## Configuration ⚙️  
Customize settings by editing `config.py`:
- Rate limiting parameters  
- Lockout durations  
- CAPTCHA behavior  
- Attack simulation specifics  

---

## File Structure 📁
```
Brute_Force_sim/
├── main.py
├── login_system.py
├── brute_force_attack.py
├── utils.py
├── config.py
├── users.json
└── password_list.txt
```

---

## Security Features Details 🔒

### Rate Limiting ⏱️
- Limits number of attempts within a set time  
- Blocks further tries if threshold exceeded  
- Time window resets after cooldown  

### Account Lockout 🔒
- Lockout durations increase progressively  
- Requires solving CAPTCHA before retry  

### CAPTCHA System 🤖
- Math-based challenges  
- Triggered after 3 failed attempts and post-lockout  
- Must be solved correctly to continue  

### Password Security 🔐
- SHA-256 hashing of passwords  
- Stored securely in JSON file  
- No plaintext passwords saved  

---

## Real-World Security Practices 🌍

> 🔒 **Note:** Real-world systems often implement permanent account locks, identity verification, multi-factor authentication, and IP-based blocking. This simulator focuses on temporary, educational security measures.

| Real-World Systems           | This Simulator              |
|-----------------------------|----------------------------|
| Permanent account lockout    | Temporary progressive lockout |
| Identity verification       | CAPTCHA verification       |
| Multi-factor authentication | Single-factor authentication |
| IP-based blocking           | Basic rate limiting        |
| Email/SMS verification      | No external verification   |

---

## Contributing 🤝  
Issues, feature requests, and pull requests are welcome!  

---

## License 📄  
MIT License — see the LICENSE file for details.

---

<div align="center">
  <sub>Built by itspodleeeee🦆</sub>
</div>
