from http.server import HTTPServer
from database.db import MySqlConnection
from http_handler import http_request_handler


if __name__ == "__main__":
    # Creates db connection
    # db = MySqlConnection()
    # if db.get_conection_instance() is None:
    #     print("Database connection failed")
    # else:
    #     print("Database connection successful")

    # Creates and open the server
    server_ip = ""
    server_port = 8008
    server_address = (server_ip, server_port)
    http_handler = http_request_handler.Server
    httpd = HTTPServer(server_address, http_handler)

    try:
        print("Starting httpd on port %d..." % server_port)
        httpd.serve_forever()
    except Exception as e:
        print("Server terminated")
        print("Database connection terminated")
        MySqlConnection.close_conection()
    except KeyboardInterrupt:
        print("Server terminated")
        print("Database connection terminated")
        MySqlConnection.close_conection()
