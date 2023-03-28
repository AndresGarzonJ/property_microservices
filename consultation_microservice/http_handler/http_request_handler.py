from http.server import BaseHTTPRequestHandler
from controller.property_controller import PropertyController
import json


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        """Sets the value of HTTP headers"""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        """Send HTTP response to GET request"""
        response = None
        error = None

        try:
            # Section Main ("/")
            if (not self.path or self.path == "/"):
                response, error = (
                    json.dumps(
                        {
                            "title": "Main Page",
                            "description": "API REST",
                            "useCases": {
                                            "properties": "/property",
                                            "optional filters": "/property" +
                                            "?city=xxxx" +
                                            "&state=<en_venta, pre_venta, " +
                                            "vendido>" +
                                            "&year=xxxx"
                                        }
                        }
                    ),
                    None,
                )
            # Properties Section ("/property")
            elif self.path.split("?")[0] == "/property":
                try:
                    # Create a list
                    filters = self.path.split("?")

                    # Removes element 0, i.e. /property
                    filters.pop(0)

                    # Check if there are more elements
                    if len(filters) > 0:
                        # Converts the filter list to a dictionary
                        filters = Server.convert_filters_to_dict(filters[0])

                        # Obtains the properties according to the filters
                        response, error = PropertyController.get_properties(
                            **filters)
                    else:
                        # Obtains all the properties
                        response, error = PropertyController.get_properties()
                except Exception as e:
                    response = json.dumps(
                        {
                            "msg": "An error has occurred",
                            "error detail": f"{e}"
                        }
                    )
        except Exception as e:
            response = json.dumps(
                {
                    "msg": "An error has occurred: " + f"{e}"
                }
            )

        # Sets HTTP headers
        self.do_HEAD()
        # Sends the response data to the client through the socket
        self.wfile.write(bytes(response if response else "", "utf-8"))

    @classmethod
    def convert_filters_to_dict(cls, filters):
        """Convert a list of filters to a dictionary

        Args:
            filters (list)

        Returns:
            dict_filters (dictionary)
        """
        dict_filters = {}
        dict_filters = {key: int(value) if value.isdigit() else value
                        for key, value in [pair.split('=')
                        for pair in filters.split('&')]}
        return dict_filters
