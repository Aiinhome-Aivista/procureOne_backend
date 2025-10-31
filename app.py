from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



PROFILE_MICROSERVICES_URL = '/VendorMicroservices'
PROFILE_MICROSERVICES_URL = '/RequisitonMicroservices'
PROFILE_MICROSERVICES_URL = '/BidselectionMicroservices'


@app.route('/', methods=['GET'])
def health():
    return "Hello World ! ProcureOne is working Fine "




if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=3005) 