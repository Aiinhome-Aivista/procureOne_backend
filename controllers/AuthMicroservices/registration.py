import bcrypt
import datetime
from flask import request, jsonify
from database.db_handler import get_db_connection


def register_controller():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        email = data.get('email')

        if not all([username, password, role, email]):
            return jsonify({
                "isSuccess": False,
                "message": "Missing required fields",
                "statusCode": 400
            }), 400

        # Validate role
        valid_roles = ['Admin', 'Manager', 'Lead', 'Vendor']
        if role not in valid_roles:
            return jsonify({
                "isSuccess": False,
                "message": f"Invalid role. Must be one of {valid_roles}",
                "statusCode": 400
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if username already exists
        cursor.execute("SELECT * FROM user_master WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({
                "isSuccess": False,
                "message": "Username already exists",
                "statusCode": 409
            }), 409

        # Encrypt password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert new user
        insert_query = """
            INSERT INTO user_master (username, password_hash, role, email, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (username, hashed_password, role, email, datetime.datetime.now()))
        conn.commit()

        return jsonify({
            "isSuccess": True,
            "message": "User registered successfully",
            "data": {
                "username": username,
                "role": role,
                "email": email
            },
            "statusCode": 200
        }), 200
    except Exception as e:
        return jsonify({
            "isSuccess": False,
            "message": str(e),
            "statusCode": 500
        }), 500	