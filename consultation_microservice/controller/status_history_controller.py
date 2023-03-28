from model.status_history import StatusHistory
from database.db import MySqlConnection, DBHelper
import json


class StatusHistoryController:
    @classmethod
    def get_status_history_lines(cls):
        """Gets all the data from the StatusHistory table

        Returns:
            response (json): Includes 'msg', and 'data'
        """
        error = None
        response = None
        cursor = MySqlConnection.get_cursor()
        try:
            list_status_history_lines = DBHelper.get_all(cursor, StatusHistory)
            response = json.dumps(
                {
                    "msg": "Query completed successfully",
                    "data": [obj.__dict__ for obj in list_status_history_lines]
                }
            )
        except Exception as e:
            error = True
            print("Error_StatusHistoryController: " + e)
        finally:
            cursor.close()
        return response, error
