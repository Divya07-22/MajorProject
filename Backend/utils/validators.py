# utils/validators.py
from marshmallow import Schema, fields, ValidationError, validates, validates_schema
import re

class UserRegistrationSchema(Schema):
    """Validation schema for user registration"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 8)
    phone_number = fields.Str(required=True)
    address = fields.Str(required=True, validate=lambda x: re.match(r'^0x[a-fA-F0-9]{40}$', x))
    
    @validates('password')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise ValidationError("Password must contain at least one number")

class UserLoginSchema(Schema):
    """Validation schema for user login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class TransactionSchema(Schema):
    """Validation schema for transaction submission"""
    amount = fields.Float(required=True, validate=lambda x: x > 0)
    Time = fields.Float()
    V1 = fields.Float()
    V2 = fields.Float()
    # Add more fields as needed

def validate_request(schema_class):
    """Decorator to validate request data"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            from flask import request, jsonify
            try:
                schema = schema_class()
                data = request.get_json()
                validated_data = schema.load(data)
                return f(*args, **kwargs)
            except ValidationError as err:
                return jsonify({"errors": err.messages}), 400
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator
