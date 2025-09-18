from functools import wraps
from flask import request, jsonify
from src.utils.exceptions import AuthenticationError

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
            
        try:
            # Add your JWT token validation logic here
            pass
        except AuthenticationError as e:
            return jsonify({'error': str(e)}), 401
            
        return f(*args, **kwargs)
    return decorated
