from flask import Flask
from flask_cors import CORS
from controllers.AuthMicroservices.login import login_controller
from controllers.AuthMicroservices.registration import register_controller

app = Flask(__name__)
CORS(app)


AUTH_MICROSERVICES_URL = '/AuthMicroservices'
VENDOR_MICROSERVICES_URL = '/VendorMicroservices'
PROFILE_MICROSERVICES_URL = '/RequisitonMicroservices'
PROFILE_MICROSERVICES_URL = '/BidselectionMicroservices'


@app.route('/', methods=['GET'])
def health():
    return "Hello World ! ProcureOne is working Fine "


# Login Api
@app.route(AUTH_MICROSERVICES_URL + '/v1/login', methods=['POST'])
def login():
    return login_controller()

# Registration Api
@app.route(AUTH_MICROSERVICES_URL + '/v1/register', methods=['POST'])
def register():
    return register_controller()    



if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=3005) 