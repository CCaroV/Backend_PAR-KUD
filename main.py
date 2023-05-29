from routes.parking import routes_parking
from routes.token import routes_token
from routes.users import *

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(routes_user)
app.register_blueprint(routes_user_auth)
app.register_blueprint(routes_SUser)
app.register_blueprint(routes_token)
app.register_blueprint(routes_parking)


@app.route("/", methods=['GET'])
def test():
    json = {}
    json["message"] = "Server running ..."
    return jsonify(json)


if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running : " + "http://" + dataConfig["host"] + ":" + str(dataConfig["port"]))
    app.run()
