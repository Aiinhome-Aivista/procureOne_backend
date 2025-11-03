import jwt
import bcrypt
import datetime
from flask import request, jsonify
from database.db_handler import get_db_connection
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_TOKEN_EXPIRE_MINUTES


def login_controller():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "isSuccess": False,
                "message": "Username or password missing",
                "statusCode": 400
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check user_master table first
        cursor.execute("SELECT * FROM user_master WHERE email = %s OR username = %s", (username, username))
        user = cursor.fetchone()

        if not user:
            return jsonify({
                "isSuccess": False,
                "message": "Invalid username or password",
                "statusCode": 401
            }), 401

        # Verify password
        stored_password = user.get("password") or user.get("password_hash")
        if not stored_password:
            return jsonify({
                "isSuccess": False,
                "message": "Password field missing in database",
                "statusCode": 500
            }), 500

        # Check password (supports both hashed and plain text for now)
        password_matches = (
            bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8"))
            if stored_password.startswith("$2b$")
            else password == stored_password
        )

        if not password_matches:
           return jsonify({
                "isSuccess": False,
                "message": "Invalid username or password",
                "statusCode": 401
            }), 401

        # Generate JWT token
        access_token = jwt.encode({
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        }, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


        refresh_token = jwt.encode({
            "user_id": user["user_id"],
            "username": user["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
        }, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        return jsonify({
            "isSuccess": True,
            "message": "Login successful",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_id": user["user_id"],
                "username": user["username"],
                "role": user["role"],
                "email": user["email"]
            },
            "statusCode": 200
        }), 200

    except Exception as e:
            return jsonify({
                "isSuccess": False,
                "message": str(e),
                "statusCode": 500
            }), 500
