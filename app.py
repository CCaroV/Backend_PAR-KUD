from flask_cors import CORS

from routes.Auth import routes_user_auth
from routes.parking import routes_parking
from routes.reservas import routes_reserve
from routes.supAdmin import routes_SUser
from routes.token import routes_token
from routes.users import *

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True,
            headers=['Authorization'],
            expose_headers='Authorization')

app.register_blueprint(routes_user)
app.register_blueprint(routes_user_auth)
app.register_blueprint(routes_SUser)
app.register_blueprint(routes_token)
app.register_blueprint(routes_parking)
app.register_blueprint(routes_reserve)

@app.route("/", methods=['GET'])
def test():
    json = {}
    json["message"] = "Server running ..."
    return jsonify(json)


if __name__ == '__main__':
    app.run(port=5000)
