import json
from flask import request, jsonify
from database.db_handler import get_db_connection

def get_countries_controller():
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        
        # Call the stored procedure for countries
        cur.callproc('sp_get_countries')
        
        # Get the result from stored procedure
        for result in cur.stored_results():
            data = result.fetchone()
        
        cur.close()
        conn.close()
        
        if data and data['status'] == 'success':
            countries = json.loads(data['data']) if isinstance(data['data'], str) else data['data']
            return jsonify({
                "status": data['status'],
                "statusCode": data['statusCode'],
                "message": data['message'],
                "data": countries
            }), data['statusCode']
        else:
            return jsonify({
                "status": "failed",
                "statusCode": 404,
                "message": "No countries found",
                "data": []
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "statusCode": 500,
            "message": "Failed to fetch countries",
            "error": str(e),
            "data": []
        }), 500
