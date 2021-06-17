from app import app
from datetime import datetime;

import logging, sys, json_logging, flask

if __name__=="__main__":
    json_logging.init_flask(enable_json=True)
    json_logging.init_request_instrument(app)
    app.run(debug=True, host='0.0.0.0', port=8444)
