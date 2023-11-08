from dataclasses import dataclass, field
from datetime import datetime
from scripts.py.mysqlDB import Table


@dataclass
class Users(Table):
    """
    A class representing the Users table.

    Attributes:
        id: The ID of the user.
        username: The username of the user.
        password: The password of the user.
        full_name: The full name of the user.
        email: The email address of the user.
        phone_number: The phone number of the user.
        home_address: The home address of the user.
        is_admin: Flag to indicate if the user is an admin.
        
    """

    id: int = field(default=0, metadata={'primary_key': True})
    username: str = field(default='', metadata={'unique': True})
    salt: str = field(default='')
    password: str = field(default='', metadata={'hashed': True})
    full_name: str = field(default='', metadata={'PII': True})
    email: str = field(default='', metadata={'PII': True})
    phone_number: str = field(default='', metadata={'PII': True})
    home_address: str = field(default='', metadata={'PII': True})
    is_admin: bool = field(default=False)
    

    @classmethod
    def create_table(cls, db_inst, print_output=False):
        """
        Creates the Users table in the database.

        Args:
            db_inst: The instance of myDB class to execute the query.
            print_output: Flag to print the query before execution (default: False).

        Returns:
            None.
        """
        super().create_table(db_inst, print_output)
        # Add additional logic specific to the Users table if needed


    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            The string representation of the object.
        """
        attributes = ", ".join([f"  \n  - {attr}: {getattr(self, attr)}" for attr in self.__dict__])
        return f"\n \n {attributes}"


    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            The string representation of the object.
        """
        return self.__repr__()
