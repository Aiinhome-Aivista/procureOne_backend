import json
from flask import request, jsonify
from database.db_handler import get_db_connection


def get_cities_controller():
    try:
        data = request.json
        state_id = data.get('stateid')
        
        if not state_id:
            return jsonify({
                "status": "failed",
                "statusCode": 400,
                "message": "State ID is required",
                "data": []
            }), 400
        
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        
        # Call the stored procedure for cities
        cur.callproc('sp_get_cities_by_state', [state_id])
        
        # Get the result from stored procedure
        for result in cur.stored_results():
            data = result.fetchone()
        
        cur.close()
        conn.close()
        
        if data and data['status'] == 'success':
            cities = json.loads(data['data']) if isinstance(data['data'], str) else data['data']
            return jsonify({
                "status": data['status'],
                "statusCode": data['statusCode'],
                "message": data['message'],
                "data": cities
            }), data['statusCode']
        else:
            return jsonify({
                "status": "failed",
                "statusCode": 404,
                "message": data.get('message', 'No cities found'),
                "data": []
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "statusCode": 500,
            "message": "Failed to fetch cities",
            "error": str(e),
            "data": []
        }), 500