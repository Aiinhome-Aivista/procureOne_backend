import firebase_admin
from flask import jsonify,request
from firebase_admin import credentials, messaging

cred = credentials.Certificate("firebaseNotification/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def send_push_notification():
    try:
        data = request.get_json()
        token = data.get("token")
        title = data.get("title")
        body = data.get("body")

        # Validate required fields
        if not token or not title or not body:
            return jsonify({
                "isSuccess": False,
                "message": "Missing required fields: token, title, or body",
                "statusCode": 400
            }), 400

        # Prepare and send notification
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token
        )

        response = messaging.send(message)
        print("Notification sent:", response)

        return jsonify({
            "isSuccess": True,
            "message": "Notification sent successfully!",
            "statusCode": 200
        }), 200

    except Exception as e:
        return jsonify({
            "isSuccess": False,
            "message": str(e),
            "statusCode": 500
        }), 500