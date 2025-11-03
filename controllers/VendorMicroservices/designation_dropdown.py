from flask import Flask, jsonify
from database.db_handler import get_db_connection  


def get_designations_controller():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Call stored procedure
        cursor.callproc("sp_get_designations")

        # Fetch result set from the stored procedure
        for result in cursor.stored_results():
            data = result.fetchone()

        cursor.close()
        conn.close()

        if not data:
            return jsonify({
                "isSuccess": False,
                "statusCode": 404,
                "message": "No Designations found.",
                "data": []
            }), 404

       
        import json
        parsed_data = []
        if data.get("data"):
            try:
                parsed_data = json.loads(data["data"])
            except Exception:
                parsed_data = []

        response = {
            "isSuccess": True,
            "statusCode": data.get("statusCode", 200),
            "message": data.get("message", "Designations fetched successfully."),
            "data": parsed_data
        }

        return jsonify(response), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "isSuccess": False,
            "statusCode": 500,
            "message": "Internal server error.",
            "error": str(e)
        }), 500

