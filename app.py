from flask import Flask
from flask_cors import CORS
from controllers.AuthMicroservices.login import login_controller
from firebaseNotification.send_notification import send_push_notification
from controllers.AuthMicroservices.registration import register_controller
from controllers.VendorMicroservices.city_dropdown import get_cities_controller
from controllers.VendorMicroservices.state_dropdown import get_states_controller
from controllers.VendorMicroservices.country_dropdown import get_countries_controller
from controllers.VendorMicroservices.vendor_registration import vendor_register_controller
from controllers.VendorMicroservices.designation_dropdown import get_designations_controller
from controllers.VendorMicroservices.business_types_dropdown import get_business_types_controller
from controllers.VendorMicroservices.industry_categories_dropdown import get_industry_categories_controller
from controllers.VendorMicroservices.legal_proof_of_company_existence_dropdown import get_legal_proof_of_company_existence_controller


app = Flask(__name__)
CORS(app)

BASE_URL_V1 = '/v1'
AUTH_MICROSERVICES_URL = BASE_URL_V1 + '/AuthMicroservices'
VENDOR_MICROSERVICES_URL = BASE_URL_V1 +'/VendorMicroservices'
PROFILE_MICROSERVICES_URL = BASE_URL_V1 +'/RequisitonMicroservices'
PROFILE_MICROSERVICES_URL = BASE_URL_V1 + '/BidselectionMicroservices'


@app.route('/', methods=['GET'])
def health():
    return "Hello World ! ProcureOne is working Fine "

# send notification api for testing
@app.route('/send-notification', methods=['POST'])
def send_notification_route():
    return send_push_notification()



# Login Api
@app.route(AUTH_MICROSERVICES_URL + '/login', methods=['POST'])
def login():
    return login_controller()

# Registration Api
@app.route(AUTH_MICROSERVICES_URL + '/register', methods=['POST'])
def register():
    return register_controller()



# vendor registration
@app.route(VENDOR_MICROSERVICES_URL + '/vendor_register', methods=['POST'])
def vendor_register():
    return vendor_register_controller()

# Business Types
@app.route(VENDOR_MICROSERVICES_URL + '/business_types', methods=["GET"])    
def get_business_types():
    return get_business_types_controller()

# Industry Categorie
@app.route(VENDOR_MICROSERVICES_URL + '/industry_categories', methods=["GET"])
def get_industry_categories():
    return get_industry_categories_controller()    

# Designations
@app.route(VENDOR_MICROSERVICES_URL + '/designations', methods=["GET"])    
def get_designations_controller_():
    return get_designations_controller()

# Legal proofs
@app.route(VENDOR_MICROSERVICES_URL + '/legal_proofs', methods=["GET"])    
def get_legal_proof_of_company_existence_controller_():
    return get_legal_proof_of_company_existence_controller()

# Country API 
@app.route(VENDOR_MICROSERVICES_URL + '/countries', methods=['GET'])
def countries():
    return get_countries_controller()

# State API 
@app.route(VENDOR_MICROSERVICES_URL + '/states', methods=['POST'])
def states():
    return get_states_controller()    

# City API 
@app.route(VENDOR_MICROSERVICES_URL + '/cities', methods=['POST'])
def cities():
    return get_cities_controller()



if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=3005) 