import os
import flask
import mcstatus
import dotenv
import subprocess
import traceback

server_db = {
    'lobby': {'host': '127.0.0.1', 'rcon_port': 25766, 'port': 25566},
    'survival': {'host': '127.0.0.1', 'rcon_port': 25767, 'port': 25567},
    'boxpvp': {'host': '127.0.0.1', 'rcon_port': 25768, 'port': 25568},
    'dev': {'host': '127.0.0.1', 'rcon_port': 25769, 'port': 25569}
}

dotenv.load_dotenv()
RCON_PASSWORD = os.environ.get("rcon_password")
BIND_IP = os.environ.get("bind_ip")
BIND_PORT = os.environ.get("bind_port")

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
                ping = mcstatus.JavaServer.lookup(f"{data['host']}:{data['port']}").ping()

                result[server] = int(round(float(ping), 2)) * 100
            except (ConnectionRefusedError, TimeoutError, OSError) as ex:
                result[server] = str(-1)

        return result

    data = server_db[server_name]
    try:
        result = mcstatus.JavaServer(data['host'], data['port'])
    except (ConnectionRefusedError, TimeoutError, OSError) as ex:
        result = str(-1)

    return result


@app.route("/")
def main():
    return flask.render_template("index.html")


@app.route("/manage/<server_name>/<operation>", methods=['POST'])
def manage_server(server_name, operation):
    if operation == "stop":
        subprocess.Popen(["screen", "-S", f"{server_name}", "-X stuff", '"stop\n"'])
    elif operation == "restart":
        subprocess.Popen(["screen", "-S", f"{server_name}", "-X stuff", '"restart\n"'])
    elif operation == 'start':
        subprocess.Popen([f'/mc_scripts/{server_name}.sh'], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
        return flask.jsonify({'code': 'ok'})
    else:
        return flask.jsonify({'code': 'wrongoperation'})

    return flask.jsonify({'code': 'ok'}), 200


app.run(host=BIND_IP, port=BIND_PORT)
