import os
import time
import flask
import mcstatus
import dotenv
import subprocess
import traceback
import server_parser

dotenv.load_dotenv()
BIND_IP = os.environ.get("bind_ip")
BIND_PORT = os.environ.get("bind_port")
SERVERS_DIRECTORY = os.environ.get("servers_directory")

server_db = server_parser.get_minecraft_servers(SERVERS_DIRECTORY)

app = flask.Flask(__name__)


@app.errorhandler(500)
def error500_handler(e):
    return flask.jsonify({'code': 'error', 'details': str(type(e).__name__), 'traceback': traceback.format_exc()}), 500


@app.route("/getServerStatus/<server_name>")
def get_server_status(server_name='all'):
    if server_name == "all":
        result = {}
        for server in server_db:
            try:
                data = server_db[server]
                ping = mcstatus.JavaServer.lookup(f"{data['server-ip']}:{data['server-port']}").ping()

                result[server] = int(round(float(ping), 2)) * 10
            except (ConnectionRefusedError, TimeoutError, OSError) as ex:
                result[server] = str(-1)

        return result

    data = server_db[server_name]
    try:
        result = mcstatus.JavaServer(data['server-ip'], data['server-port'])
    except (ConnectionRefusedError, TimeoutError, OSError) as ex:
        result = str(-1)

    return result

@app.route("/")
def main():
    return flask.render_template("index.html")


@app.route("/manage/<operation>", methods=['POST'])
def manage_server(operation):

    server_list = flask.request.json.get("server_list")
    print(server_list)
    try:
        for server_name in server_list:

            screen_name = server_db.get(server_name).get("screen-name", None)

            if operation == "stop":
                subprocess.Popen(["screen", "-S", f"{screen_name}", "-X", "stuff", '^C'])

            elif operation == "restart":
                subprocess.Popen(["screen", "-S", f"{screen_name}", "-X", "stuff", '^C'])

                x = 0
                while x < 10:
                    x += 1
                    status = get_server_status(server_name)
                    if status == -1:
                        break
                    time.sleep(1)

                subprocess.Popen([f'/mc_scripts/{server_name}.sh'], stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)

            elif operation == 'start':
                subprocess.Popen([f'/mc_scripts/{server_name}.sh'], stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
            else:
                return flask.jsonify({'code': 'wrongoperation'})
    except FileNotFoundError as ex:
        return flask.jsonify({'code': 'wrong_screen_name', 'data': f"{ex}"}), 400
    return flask.jsonify({'code': 'ok'}), 200


app.run(host=BIND_IP, port=BIND_PORT)
