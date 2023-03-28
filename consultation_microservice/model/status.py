class Status:

    db_name = "status"
    fields = ["id", "name", "label"]

    id_: int
    name: str
    label: str

    def __init__(self, **kwargs) -> None:
        self.id_ = kwargs.get("id")
        self.name = kwargs.get("name")
        self.label = kwargs.get("label")