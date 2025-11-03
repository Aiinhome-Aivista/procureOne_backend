from flask import Flask
from flask_cors import CORS
from controllers.AuthMicroservices.login import login_controller
from controllers.AuthMicroservices.registration import register_controller
from controllers.VendorMicroservices.vendor_registration import vendor_register_controller
from firebaseNotification.send_notification import send_push_notification

app = Flask(__name__)
CORS(app)


AUTH_MICROSERVICES_URL = '/AuthMicroservices'
VENDOR_MICROSERVICES_URL = '/VendorMicroservices'
PROFILE_MICROSERVICES_URL = '/RequisitonMicroservices'
PROFILE_MICROSERVICES_URL = '/BidselectionMicroservices'


@app.route('/', methods=['GET'])
def health():
    return "Hello World ! ProcureOne is working Fine "

# send notification api for testing
@app.route('/v1/send-notification', methods=['POST'])
def send_notification_route():
    return send_push_notification()



# Login Api
@app.route(AUTH_MICROSERVICES_URL + '/v1/login', methods=['POST'])
def login():
    return login_controller()

# Registration Api
@app.route(AUTH_MICROSERVICES_URL + '/v1/register', methods=['POST'])
def register():
    return register_controller()

# vendor registration
@app.route(VENDOR_MICROSERVICES_URL + '/v1/vendor_register', methods=['POST'])
def vendor_register():
    return vendor_register_controller()



if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=3005) 