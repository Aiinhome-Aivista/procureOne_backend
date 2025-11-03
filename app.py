from flask import Flask
from flask_cors import CORS
from controllers.VendorMicroservices.login import login_controller

app = Flask(__name__)
CORS(app)



VENDOR_MICROSERVICES_URL = '/VendorMicroservices'
PROFILE_MICROSERVICES_URL = '/RequisitonMicroservices'
PROFILE_MICROSERVICES_URL = '/BidselectionMicroservices'


@app.route('/', methods=['GET'])
def health():
    return "Hello World ! ProcureOne is working Fine "


# Login Api
@app.route(VENDOR_MICROSERVICES_URL + '/v1/login', methods=['POST'])
def login():
    return login_controller()



if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=3005) 