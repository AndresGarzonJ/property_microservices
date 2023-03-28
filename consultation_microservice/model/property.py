class Property(object):
    """Represents a property

    Attributes table:
        db_name (string): Table name
        fields (list): Table fields

    Attributes of property object:
        id_ (integer): Property identifier
        address (string): Property address
        city (string): City of property location
        price (float): Property price
        description (string): Property description
        year (integer): Year of construction of the property
    """

    db_name = "property"
    fields = ["id", "address", "city", "price", "description", "year"]

    # Attributes
    id_: int
    address: str
    city: str
    price: float
    description: str
    year: int

    # Entrypoint - Constructor function - To instantiate the class
    def __init__(self, **kwargs):
        self.id_ = kwargs.get("id")
        self.address = kwargs.get("address")
        self.city = kwargs.get("city")
        self.price = kwargs.get("price")
        self.description = kwargs.get("description")
        self.year = kwargs.get("year")
