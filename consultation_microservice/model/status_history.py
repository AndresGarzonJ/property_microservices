class StatusHistory:
    """Represents the status of a property

    Attributes table:
        db_name (string): Table name
        fields (list): Table fields

    Attributes of property object:
        id_ (integer): Identifier of a state of a property
        property_id (integer): Property identifier
        status_id (integer): Status identifier
        update_date (string): Date of property status update
    """

    db_name = "status_history"
    fields = ["id", "property_id", "status_id", "update_date"]

    id_: int
    property_id: int
    status_id: int
    update_date: str

    def __init__(self, **kwargs) -> None:
        self.id_ = kwargs.get("id")
        self.property_id = kwargs.get("property_id")
        self.status_id = kwargs.get("status_id")
        self.update_date = kwargs.get("update_date")
