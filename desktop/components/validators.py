"""
Form validation utilities for desktop application.

This module provides reusable validation functions for common form fields
like usernames, emails, passwords, and task titles.
"""

import re
from typing import Optional, Tuple


class Validator:
    """Collection of static validation methods."""
    
    # Validation constants
    MIN_USERNAME_LENGTH = 3
    MIN_PASSWORD_LENGTH = 6
    MIN_TASK_TITLE_LENGTH = 3
    
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, Optional[str]]:
        """
        Validate username field.
        
        Rules:
            - Required
            - Minimum 3 characters
            
        Args:
            username: Username string to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
            
        Example:
            >>> is_valid, error = Validator.validate_username("ab")
            >>> print(error)
            'Username must be at least 3 characters'
        """
        if not username:
            return False, "Username is required"
        
        if len(username.strip()) < Validator.MIN_USERNAME_LENGTH:
            return False, f"Username must be at least {Validator.MIN_USERNAME_LENGTH} characters"
        
        return True, None
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """
        Validate email field.
        
        Rules:
            - Required
            - Valid email format (basic regex check)
            
        Args:
            email: Email string to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
            
        Example:
            >>> is_valid, error = Validator.validate_email("invalid")
            >>> print(error)
            'Invalid email format'
        """
        if not email:
            return False, "Email is required"
        
        if not re.match(Validator.EMAIL_REGEX, email):
            return False, "Invalid email format"
        
        return True, None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password field.
        
        Rules:
            - Required
            - Minimum 6 characters
            
        Args:
            password: Password string to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
            
        Example:
            >>> is_valid, error = Validator.validate_password("abc")
            >>> print(error)
            'Password must be at least 6 characters'
        """
        if not password:
            return False, "Password is required"
        
        if len(password) < Validator.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {Validator.MIN_PASSWORD_LENGTH} characters"
        
        return True, None
    
    @staticmethod
    def validate_task_title(title: str) -> Tuple[bool, Optional[str]]:
        """
        Validate task title field.
        
        Rules:
            - Required
            - Minimum 3 characters (after trimming)
            
        Args:
            title: Task title string to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
            
        Example:
            >>> is_valid, error = Validator.validate_task_title("  a ")
            >>> print(error)
            'Task title must be at least 3 characters'
        """
        if not title:
            return False, "Task title is required"
        
        if len(title.strip()) < Validator.MIN_TASK_TITLE_LENGTH:
            return False, f"Task title must be at least {Validator.MIN_TASK_TITLE_LENGTH} characters"
        
        return True, None
    
    @staticmethod
    def validate_all_fields(fields: dict) -> Tuple[bool, dict]:
        """
        Validate multiple fields at once.
        
        Args:
            fields: Dictionary with field names as keys and values as tuples (value, validator_function)
            
        Returns:
            Tuple[bool, dict]: (all_valid, {field_name: error_message})
            
        Example:
            >>> fields = {
            ...     'username': ('ab', Validator.validate_username),
            ...     'email': ('test@email.com', Validator.validate_email)
            ... }
            >>> is_valid, errors = Validator.validate_all_fields(fields)
            >>> print(errors['username'])
            'Username must be at least 3 characters'
        """
        errors = {}
        all_valid = True
        
        for field_name, (value, validator_func) in fields.items():
            is_valid, error = validator_func(value)
            if not is_valid:
                errors[field_name] = error
                all_valid = False
        
        return all_valid, errors


def create_realtime_validator(field: 'ft.TextField', validator_func: callable, page: 'ft.Page'):
    """
    Create a real-time validation handler for a TextField.
    
    This function returns an on_change callback that validates the field
    and updates its error_text in real-time.
    
    Args:
        field: Flet TextField to validate
        validator_func: Validation function from Validator class
        page: Flet Page instance (for update calls)
        
    Returns:
        callable: on_change event handler
        
    Example:
        >>> username_field = ft.TextField(label="Username")
        >>> username_field.on_change = create_realtime_validator(
        ...     username_field,
        ...     Validator.validate_username,
        ...     page
        ... )
    """
    def on_change_handler(e):
        if field.value:
            is_valid, error = validator_func(field.value)
            field.error_text = error if not is_valid else None
        else:
            field.error_text = None
        page.update()
    
    return on_change_handler
