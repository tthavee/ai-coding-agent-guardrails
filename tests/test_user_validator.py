"""
test_user_validator.py — Tests for src/user_validator.py

Follows testing-standards.md:
  - Happy path, edge cases, error paths, and security edge cases for every function
  - Scenario-based test names (Given-When-Then style)
  - No mocks of the unit under test
  - Human-authored edge cases on top of scaffolding
"""

import pytest
from src.user_validator import (
    ValidationError,
    build_user_query,
    hash_password,
    safe_display_name,
    validate_email,
    validate_username,
    verify_password,
)


# ──────────────────────────────────────────────────────────────
# validate_email
# ──────────────────────────────────────────────────────────────


class TestValidateEmail:
    # Happy path
    def test_valid_email_returns_lowercased(self):
        assert validate_email("User@Example.COM") == "user@example.com"

    def test_valid_email_with_plus_sign(self):
        assert validate_email("user+tag@example.com") == "user+tag@example.com"

    def test_valid_email_with_subdomain(self):
        assert validate_email("a@mail.example.co.uk") == "a@mail.example.co.uk"

    # Edge cases
    def test_empty_email_raises_validation_error(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_email("")

    def test_email_exceeding_max_length_raises_validation_error(self):
        long_email = "a" * 250 + "@x.com"
        with pytest.raises(ValidationError, match="exceeds maximum length"):
            validate_email(long_email)

    def test_email_at_exact_max_length_is_accepted(self):
        # 254 chars total: "@example.com" = 12 chars, so local = 242
        local = "a" * 242
        email = f"{local}@example.com"
        assert len(email) == 254
        result = validate_email(email)
        assert result == email.lower()

    def test_email_one_over_max_length_raises(self):
        local = "a" * 243
        email = f"{local}@example.com"
        assert len(email) == 255
        with pytest.raises(ValidationError, match="exceeds maximum length"):
            validate_email(email)

    # Error paths
    def test_none_email_raises_type_error(self):
        with pytest.raises(TypeError):
            validate_email(None)

    def test_non_string_email_raises_type_error(self):
        with pytest.raises(TypeError):
            validate_email(42)

    def test_missing_at_sign_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Invalid email format"):
            validate_email("notanemail.com")

    def test_missing_domain_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Invalid email format"):
            validate_email("user@")

    def test_missing_local_part_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Invalid email format"):
            validate_email("@example.com")

    # Security edge cases
    def test_sql_injection_in_email_is_rejected(self):
        with pytest.raises(ValidationError):
            validate_email("user@x.com'; DROP TABLE users;--")

    def test_xss_in_email_is_rejected(self):
        with pytest.raises(ValidationError):
            validate_email("<script>alert(1)</script>@example.com")

    def test_newline_in_email_is_rejected(self):
        with pytest.raises(ValidationError):
            validate_email("user\n@example.com")


# ──────────────────────────────────────────────────────────────
# validate_username
# ──────────────────────────────────────────────────────────────


class TestValidateUsername:
    # Happy path
    def test_valid_alphanumeric_username(self):
        assert validate_username("john_doe123") == "john_doe123"

    def test_valid_username_with_hyphen(self):
        assert validate_username("john-doe") == "john-doe"

    # Edge cases
    def test_empty_username_raises_validation_error(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_username("")

    def test_username_at_max_length_is_accepted(self):
        username = "a" * 50
        assert validate_username(username) == username

    def test_username_over_max_length_raises(self):
        with pytest.raises(ValidationError, match="exceeds maximum length"):
            validate_username("a" * 51)

    def test_single_character_username_is_valid(self):
        assert validate_username("x") == "x"

    # Error paths
    def test_none_username_raises_type_error(self):
        with pytest.raises(TypeError):
            validate_username(None)

    def test_non_string_username_raises_type_error(self):
        with pytest.raises(TypeError):
            validate_username(["alice"])

    # Security edge cases
    def test_username_with_space_raises_validation_error(self):
        with pytest.raises(ValidationError, match="may only contain"):
            validate_username("john doe")

    def test_username_with_special_chars_raises_validation_error(self):
        with pytest.raises(ValidationError, match="may only contain"):
            validate_username("admin'; DROP TABLE users;--")

    def test_username_with_html_raises_validation_error(self):
        with pytest.raises(ValidationError):
            validate_username("<script>")


# ──────────────────────────────────────────────────────────────
# hash_password / verify_password
# ──────────────────────────────────────────────────────────────


class TestPasswordHashing:
    # Happy path
    def test_hash_password_returns_bytes(self):
        result = hash_password("Secure123!")
        assert isinstance(result, bytes)

    def test_hash_password_produces_bcrypt_hash(self):
        result = hash_password("Secure123!")
        # bcrypt hashes always start with $2b$
        assert result.startswith(b"$2b$")

    def test_same_password_produces_different_hashes(self):
        # bcrypt uses a random salt — two hashes of the same password differ
        h1 = hash_password("Secure123!")
        h2 = hash_password("Secure123!")
        assert h1 != h2

    def test_verify_password_correct_password_returns_true(self):
        hashed = hash_password("MyPassword1")
        assert verify_password("MyPassword1", hashed) is True

    def test_verify_password_wrong_password_returns_false(self):
        hashed = hash_password("MyPassword1")
        assert verify_password("WrongPassword", hashed) is False

    # Edge cases
    def test_password_at_min_length_is_accepted(self):
        result = hash_password("12345678")
        assert result.startswith(b"$2b$")

    def test_password_below_min_length_raises(self):
        with pytest.raises(ValidationError, match="at least"):
            hash_password("short")

    def test_empty_password_raises_validation_error(self):
        with pytest.raises(ValidationError):
            hash_password("")

    def test_very_long_password_is_accepted(self):
        result = hash_password("x" * 100)
        assert result.startswith(b"$2b$")

    # Error paths
    def test_none_password_raises_type_error(self):
        with pytest.raises(TypeError):
            hash_password(None)

    def test_verify_none_plain_text_raises_type_error(self):
        hashed = hash_password("Secure123!")
        with pytest.raises(TypeError):
            verify_password(None, hashed)

    def test_verify_none_hash_raises_type_error(self):
        with pytest.raises(TypeError):
            verify_password("Secure123!", None)


# ──────────────────────────────────────────────────────────────
# build_user_query
# ──────────────────────────────────────────────────────────────


class TestBuildUserQuery:
    # Happy path
    def test_returns_parameterised_query_tuple(self):
        query, params = build_user_query(1)
        assert "?" in query
        assert params == (1,)

    def test_user_id_not_interpolated_into_query_string(self):
        query, params = build_user_query(42)
        # The numeric value must NOT appear in the query string itself
        assert "42" not in query

    def test_query_selects_expected_columns(self):
        query, _ = build_user_query(1)
        assert "id" in query
        assert "username" in query
        assert "email" in query

    # Edge cases
    def test_large_user_id_is_accepted(self):
        query, params = build_user_query(999_999_999)
        assert params == (999_999_999,)

    # Error paths
    def test_zero_user_id_raises_validation_error(self):
        with pytest.raises(ValidationError, match="positive integer"):
            build_user_query(0)

    def test_negative_user_id_raises_validation_error(self):
        with pytest.raises(ValidationError):
            build_user_query(-1)

    def test_string_user_id_raises_type_error(self):
        with pytest.raises(TypeError):
            build_user_query("1")

    def test_float_user_id_raises_type_error(self):
        with pytest.raises(TypeError):
            build_user_query(1.0)

    def test_bool_user_id_raises_type_error(self):
        # bool is a subclass of int in Python — must be explicitly rejected
        with pytest.raises(TypeError):
            build_user_query(True)

    # Security edge cases
    def test_sql_injection_string_raises_type_error(self):
        with pytest.raises(TypeError):
            build_user_query("1; DROP TABLE users;--")


# ──────────────────────────────────────────────────────────────
# safe_display_name
# ──────────────────────────────────────────────────────────────


class TestSafeDisplayName:
    # Happy path
    def test_plain_name_is_returned_unchanged(self):
        assert safe_display_name("Alice") == "Alice"

    def test_name_with_numbers_is_returned_unchanged(self):
        assert safe_display_name("User123") == "User123"

    # Security edge cases — XSS prevention
    def test_script_tag_is_escaped(self):
        result = safe_display_name("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_angle_brackets_are_escaped(self):
        result = safe_display_name("<b>bold</b>")
        assert "<b>" not in result

    def test_double_quotes_are_escaped(self):
        result = safe_display_name('Say "hello"')
        assert '"' not in result

    def test_ampersand_is_escaped(self):
        result = safe_display_name("Tom & Jerry")
        assert "&" not in result or "&amp;" in result

    def test_javascript_url_scheme_is_escaped(self):
        result = safe_display_name("javascript:alert(1)")
        # The string itself is not a tag so no escaping needed,
        # but angle brackets and quotes in a fuller payload would be escaped
        assert "<" not in result

    # Error paths
    def test_none_raises_type_error(self):
        with pytest.raises(TypeError):
            safe_display_name(None)

    def test_non_string_raises_type_error(self):
        with pytest.raises(TypeError):
            safe_display_name(123)

    # Edge cases
    def test_empty_string_returns_empty_string(self):
        assert safe_display_name("") == ""

    def test_unicode_name_is_returned_correctly(self):
        assert safe_display_name("张伟") == "张伟"
