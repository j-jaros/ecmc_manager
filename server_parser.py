import os


def get_minecraft_servers(dir: str) -> dict:
    server_list = os.listdir(dir)
    server_list = [item for item in server_list if not item.startswith(".")]

    for server in server_list:
        # sprawdzamy czy w folderze znajduje sie plik server.properties
        srv_prop_exists = os.path.exists(f"{dir}/{server}/server.properties")
        if not srv_prop_exists:
            server_list.remove(server)

    server_data = {}
    for server in server_list:
        with open(f"/{dir}/{server}/server.properties", "r") as f:
            server_properties_lines_list = f.readlines()

            server_properties_dict = {}
            for line in server_properties_lines_list:
                line = line.replace("\n", "")
                data = line.split("=")
                if len(data) == 1:
                    continue
                server_properties_dict[data[0]] = data[1]

            server_data[server] = {'server-ip': server_properties_dict.get('server-ip', None),
                                   'server-port': int(server_properties_dict.get('server-port', None)),
                                   'screen-name': server_properties_dict.get('screen-name', None)}

    return server_data
