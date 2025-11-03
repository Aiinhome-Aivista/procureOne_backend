import json
from flask import Flask, jsonify
from database.db_handler import get_db_connection  


def get_industry_categories_controller():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Call the stored procedure
        cursor.callproc('sp_get_industry_categories')

        # Fetch result sets
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                
                data = json.loads(row.get("data", "[]"))
                
                response = {
                    "isSuccess": True,
                    "statusCode": int(row.get("statusCode", 200)),
                    "message": row.get("message", "Industry categories fetched successfully."),
                    "data": data
                }
                break
            else:
                response = {
                    "isSuccess": False,
                    "statusCode": 404,
                    "message": "No industry categories found.",
                    "data": []
                }

        cursor.close()
        conn.close()

        return jsonify(response), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "isSuccess": False,
            "statusCode": 500,
            "message": "An error occurred while fetching industry categories.",
            "error": str(e)
        }), 500



