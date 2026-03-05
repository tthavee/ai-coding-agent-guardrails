"""
user_validator.py — Sample module demonstrating AGENTS.md compliant patterns.

This module shows:
- Input validation at system boundaries
- Safe password hashing (bcrypt, not MD5/SHA1)
- Parameterized query building (no string concatenation)
- XSS-safe output encoding
- No hardcoded secrets or credentials
"""

import re
import html
import bcrypt  # generated: copilot — reviewed by: tthavee

MAX_EMAIL_LENGTH = 254  # RFC 5321 limit
MAX_USERNAME_LENGTH = 50
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128  # bcrypt silently truncates beyond 72 bytes; hard cap prevents DoS
_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


class ValidationError(ValueError):
    """Raised when user input fails validation."""


def validate_email(email: str) -> str:
    """
    Validate and normalise an email address.

    Returns the lower-cased email on success.
    Raises ValidationError on invalid input.
    """
    if email is None:
        raise TypeError("email must be a string, got None")
    if not isinstance(email, str):
        raise TypeError(f"email must be a string, got {type(email).__name__}")
    if len(email) == 0:
        raise ValidationError("Email cannot be empty")
    if len(email) > MAX_EMAIL_LENGTH:
        raise ValidationError(
            f"Email exceeds maximum length of {MAX_EMAIL_LENGTH} characters"
        )
    normalised = email.strip().lower()
    if not _EMAIL_REGEX.match(normalised):
        raise ValidationError(f"Invalid email format: {email!r}")
    return normalised


def validate_username(username: str) -> str:
    """
    Validate a username: alphanumeric plus hyphens and underscores only.

    Returns the username on success.
    Raises ValidationError on invalid input.
    """
    if username is None:
        raise TypeError("username must be a string, got None")
    if not isinstance(username, str):
        raise TypeError(f"username must be a string, got {type(username).__name__}")
    if len(username) == 0:
        raise ValidationError("Username cannot be empty")
    if len(username) > MAX_USERNAME_LENGTH:
        raise ValidationError(
            f"Username exceeds maximum length of {MAX_USERNAME_LENGTH} characters"
        )
    if not re.match(r"^[a-zA-Z0-9_\-]+$", username):
        raise ValidationError(
            "Username may only contain letters, numbers, hyphens, and underscores"
        )
    return username


def validate_password(password: str) -> str:
    """
    Validate a password meets length requirements.

    Returns the password unchanged on success.
    Raises TypeError for non-string input, ValidationError if length is out of range.
    """
    # Logic: rejects None/non-string early via TypeError; enforces MIN (8) and MAX (128)
    #        length bounds — MAX guards against bcrypt DoS on inputs > 72 bytes.
    # generated: copilot — reviewed by: <author>
    if password is None:
        raise TypeError("password must be a string, got None")
    if not isinstance(password, str):
        raise TypeError(f"password must be a string, got {type(password).__name__}")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
        )
    if len(password) > MAX_PASSWORD_LENGTH:
        raise ValidationError(
            f"Password must not exceed {MAX_PASSWORD_LENGTH} characters"
        )
    return password
    # end generated: copilot


def hash_password(plain_text: str) -> bytes:
    """
    Hash a password using bcrypt with a random salt.

    Never stores plain text. Never uses MD5 or SHA1.
    Raises ValidationError if password does not meet minimum requirements.
    """
    validate_password(plain_text)
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_text.encode("utf-8"), salt)


def verify_password(plain_text: str, hashed: bytes) -> bool:
    """
    Verify a plain-text password against a bcrypt hash.

    Returns True if the password matches, False otherwise.
    Never raises on mismatch — only raises on invalid input types.
    """
    if plain_text is None or hashed is None:
        raise TypeError("plain_text and hashed must not be None")
    return bcrypt.checkpw(plain_text.encode("utf-8"), hashed)


def build_user_query(user_id: int) -> tuple[str, tuple]:
    """
    Build a parameterised SELECT query for a user by ID.

    Returns a (query_string, params) tuple safe for use with
    any DB-API 2.0 cursor:  cursor.execute(*build_user_query(uid))

    Never concatenates user input into the query string.
    """
    if not isinstance(user_id, int) or isinstance(user_id, bool):
        raise TypeError(f"user_id must be an int, got {type(user_id).__name__}")
    if user_id <= 0:
        raise ValidationError("user_id must be a positive integer")
    query = "SELECT id, username, email FROM users WHERE id = ?"
    return query, (user_id,)


def safe_display_name(raw_name: str) -> str:
    """
    Escape a user-supplied display name for safe HTML rendering.

    Prevents XSS by escaping <, >, &, ', and " characters.
    """
    if raw_name is None:
        raise TypeError("raw_name must be a string, got None")
    if not isinstance(raw_name, str):
        raise TypeError(f"raw_name must be a string, got {type(raw_name).__name__}")
    return html.escape(raw_name, quote=True)
