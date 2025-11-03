from flask import request, jsonify 
from database.db_handler import get_db_connection


# ------------------------------
# Vendor Registration API
# ------------------------------
def vendor_register_controller():
    try:
        data = request.get_json()

        user_id = data.get('user_id')
        vendor_name = data.get('vendor_name')
        contact_person = data.get('contact_person')
        email = data.get('email')
        phone = data.get('phone')
        company_name = data.get('company_name')
        address = data.get('address')

        if not vendor_name:
            return jsonify({
                "isSuccess": False,
                "message": "Vendor name is required",
                "data": {},
                "statusCode": 400
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # --------------------------
        # Duplicate vendor check (by email or phone)
        # --------------------------
        cursor.execute("""
            SELECT vendor_id FROM vendor_master 
            WHERE email = %s OR phone = %s
        """, (email, phone))
        existing_vendor = cursor.fetchone()

        if existing_vendor:
            return jsonify({
                "isSuccess": False,
                "message": "Vendor already registered with this email or phone number",
                "data": {},
                "statusCode": 409
            }), 409


        # Call stored procedure
        cursor.callproc('sp_register_vendor', (
            user_id,
            vendor_name,
            contact_person,
            email,
            phone,
            company_name,
            address
        ))
        conn.commit()

        # Fetch the newly created vendor
        cursor.execute("""
            SELECT vendor_id, vendor_code, vendor_name, email, phone, status, user_id
            FROM vendor_master
            WHERE user_id = %s
            ORDER BY created_at DESC LIMIT 1
        """, (user_id,))
        vendor = cursor.fetchone()

        return jsonify({
            "isSuccess": True,
            "message": "Vendor registered successfully",
            "data": {
                "vendor": vendor
            },
            "statusCode": 200
        }), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "isSuccess": False,
            "message": str(e),
            "data": {},
            "statusCode": 500
        }), 500

   
