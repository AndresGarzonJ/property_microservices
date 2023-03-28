from model.status import Status
from database.db import MySqlConnection, DBHelper
from cachetools import cached, TTLCache
from datetime import timedelta, datetime


cache = TTLCache(maxsize=100, ttl=timedelta(minutes=10), timer=datetime.now)


class StatusController:
    @classmethod
    @cached(cache)
    def get_name_status_by_id(cls, id_):
        """Gets the name of the state according to a given id

        Args:
            id_ (string): State id

        Returns:
             status_by_id.name (string): Name of state
        """
        status_by_id = None
        cursor = MySqlConnection.get_cursor()
        try:
            id_ = int(id_)
            # Gets a status object according to its id
            status_by_id = DBHelper.get_by_filter(
                cursor,
                Status,
                **{"id": id_})
            status_by_id = status_by_id[0]
        except Exception as e:
            print("Error_StatusController: " + e)
        finally:
            cursor.close()
        return status_by_id.name if status_by_id else ""
