"""
AUTH MODULE - SQLite3 Database for User Authentication
Handles: DB init, user registration, login validation, session management
"""

import sqlite3
import hashlib
import os
import re
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "users.db")


def init_db():
    """Initialize the SQLite3 database and create tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name   TEXT    NOT NULL,
            username    TEXT    NOT NULL UNIQUE,
            email       TEXT    NOT NULL UNIQUE,
            password    TEXT    NOT NULL,
            created_at  TEXT    NOT NULL,
            last_login  TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            login_time  TEXT    NOT NULL,
            ip_address  TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Seed default demo account for instant portfolio/reviewer evaluation
    cursor.execute("SELECT id FROM users WHERE username = 'demo'")
    if not cursor.fetchone():
        demo_salt = "datasphere_enterprise_salt_2024"
        demo_pwd_hashed = hashlib.sha256(f"{demo_salt}Demo12345{demo_salt}".encode()).hexdigest()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO users (full_name, username, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Demo Reviewer", "demo", "demo@datasphere.local", demo_pwd_hashed, now))

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with a salt."""
    salt = "datasphere_enterprise_salt_2024"
    salted = f"{salt}{password}{salt}"
    return hashlib.sha256(salted.encode()).hexdigest()


def validate_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength. Returns (is_valid, message)."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    return True, "OK"


def register_user(full_name: str, username: str, email: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.
    Returns (success: bool, message: str)
    """
    # Validate inputs
    if not full_name.strip():
        return False, "Full name is required."
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if not validate_email(email):
        return False, "Please enter a valid email address."

    is_valid_pwd, pwd_msg = validate_password(password)
    if not is_valid_pwd:
        return False, pwd_msg

    hashed = hash_password(password)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username.lower(),))
        if cursor.fetchone():
            conn.close()
            return False, "Username already taken. Please choose another."

        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower(),))
        if cursor.fetchone():
            conn.close()
            return False, "An account with this email already exists."

        # Insert new user
        cursor.execute('''
            INSERT INTO users (full_name, username, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (full_name.strip(), username.lower().strip(), email.lower().strip(), hashed, created_at))

        conn.commit()
        conn.close()
        return True, "Account created successfully! Please login."

    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"


def login_user(identifier: str, password: str, ip_address: str = "unknown") -> tuple[bool, str, dict]:
    """
    Authenticate a user by username OR email + password.
    Returns (success: bool, message: str, user_data: dict)
    """
    hashed = hash_password(password)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Allow login via username OR email
        cursor.execute('''
            SELECT id, full_name, username, email, created_at
            FROM users
            WHERE (username = ? OR email = ?) AND password = ?
        ''', (identifier.lower().strip(), identifier.lower().strip(), hashed))

        user = cursor.fetchone()

        if not user:
            conn.close()
            return False, "Invalid username/email or password.", {}

        user_id, full_name, username, email, created_at = user

        # Update last login time
        last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (last_login, user_id))

        # Log the login event
        cursor.execute('''
            INSERT INTO login_logs (user_id, login_time, ip_address)
            VALUES (?, ?, ?)
        ''', (user_id, last_login, ip_address))

        conn.commit()
        conn.close()

        user_data = {
            "id": user_id,
            "full_name": full_name,
            "username": username,
            "email": email,
            "created_at": created_at,
            "last_login": last_login
        }
        return True, f"Welcome back, {full_name}!", user_data

    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}", {}


def get_all_users() -> list:
    """Get all registered users (for admin purposes)."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, username, email, created_at, last_login FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except sqlite3.Error:
        return []


def get_user_count() -> int:
    """Get total number of registered users."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except sqlite3.Error:
        return 0


# Initialize database on import
init_db()
