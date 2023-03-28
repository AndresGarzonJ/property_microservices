from model.property import Property
from database.db import MySqlConnection, DBHelper
import json
from controller.status_history_controller import StatusHistoryController
from controller.status_controller import StatusController


class PropertyController:

    @classmethod
    def get_properties(cls, **kwargs):
        """Obtains the properties

        Args:
            **kwargs: Filter dictionary

        Returns:
            response (json): Includes 'msg', 'count', 'data'
        """
        error = None
        response = None
        cursor = MySqlConnection.get_cursor()
        filter_by_state = "state" in kwargs.keys()

        try:
            # As "state" is in another table, we first confirm if the query
            # includes it
            if filter_by_state:
                state_to_filter = kwargs["state"]
                # Remove the "state" filter to later make the query in the
                # properties table
                del kwargs["state"]

            if len(kwargs) > 0:
                # Obtains all properties, filtering them by year and/or city
                list_properties = DBHelper.get_by_filter(
                    cursor, Property, **kwargs)
            else:
                # Gets all properties
                list_properties = DBHelper.get_all(cursor, Property)

            # Adds the "status" attribute to the object
            cls.add_actually_status(list_properties)

            # If the query includes filtering by state
            if filter_by_state:
                list_properties = cls.filter_by_status_valid_to_show(
                    list_properties, [state_to_filter,],
                )
            else:
                # Filter by all valid states
                list_properties = cls.filter_by_status_valid_to_show(
                    list_properties)

            # list_properties is a list of properties objects
            # Converts to a list of dictionaries
            data_to_return = [obj.__dict__ for obj in list_properties]
            response = json.dumps(
                {
                    "msg": "Query completed successfully",
                    "count": len(data_to_return),
                    "data": data_to_return,
                }
            )
        except Exception as e:
            print("Error_PropertyController: " + e)
        finally:
            cursor.close()
        return response, error

    @classmethod
    def add_actually_status(cls, list_properties):
        """Agrega el atributo "status" a cada property

        Args:
            list_properties (list): List of Properties
        """

        # Gets all the data from the StatusHistory table
        response, error = StatusHistoryController.get_status_history_lines()

        # Converts StatusHistory response to a dictionary
        response = json.loads(response)
        data = response["data"]

        for prop in list_properties:
            temp_prop_id = prop.id_

            def filter_property_by_id(prop, prop_id=temp_prop_id):
                """Returns True, if the id of the property is equal to prop_id
                """
                return prop["property_id"] == prop_id

            # Select property
            temp_status_by_property = list(filter(filter_property_by_id, data))

            # If there is more than one record in the StatusHistory table for
            # a property
            if len(temp_status_by_property) > 1:
                # Sorts the records in descending order according to date
                temp_status_by_property = sorted(
                    temp_status_by_property,
                    key=lambda x: x["update_date"],
                    reverse=True
                )

            if len(temp_status_by_property) > 0:
                # Adds the status attribute to the property
                # The status will be the most recently added
                prop.status = StatusController.get_name_status_by_id(
                    temp_status_by_property[0]["status_id"]
                )
            else:
                prop.status = None

    @classmethod
    def filter_by_status_valid_to_show(
        cls, list_properties, valid_states=[
            "en_venta",
            "pre_venta",
            "vendido"
            ]
    ):
        """Filter properties by valid_state

        Args:
            list_properties (list): Lista of properties
            valid_states (list): List of valid states

        Returns:
            list_properties (list): List of filtered properties
        """
        def filter_by_states(obj, valid_states=valid_states):
            """Validate that obj includes valid_states

            Args:
                obj (Object): Object property

            Returns:
                boolean
            """
            return obj.status in valid_states

        # Filter properties that have a valid_state
        list_properties = [
            element for element in filter(filter_by_states, list_properties)
        ]
        return list_properties
