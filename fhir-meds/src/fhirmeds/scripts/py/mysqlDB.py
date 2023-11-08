import mysql.connector
from dataclasses import dataclass
import os
from typing import Type
import bcrypt
from datetime import datetime


class myDB:
    """
    A class representing a database connection and query execution.

    Attributes:
        cnx: The connection to the MySQL server.
        csr: The cursor object to execute SQL queries.
    """

    def __init__(self, reset: bool = False) -> None:
        """
        Initializes a new instance of the myDB class.

        Args:
            reset: Flag indicating whether to reset the database (default: False).
        """
        # Replace the placeholders with your actual values
        host: str = "localhost"
        user: str = "root"
        password: str = os.environ["MY_SQL_PW"]
        database: str = "mysql"

        # Establish connection to the MySQL server
        self.cnx: mysql.connector.connection.MySQLConnection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object to execute SQL queries
        self.csr: mysql.connector.cursor.MySQLCursor = self.cnx.cursor()

        if reset:
            self.__call__("DROP DATABASE meds_db;")

        # Run database setup code 
        self.__call__("SHOW DATABASES;")
        self.__call__("SELECT DATABASE();")
        self.__call__("CREATE DATABASE IF NOT EXISTS meds_db;")
        self.__call__("USE meds_db;")


    
    def __call__(self, query: str, values: tuple = None, print_output: bool = False, print_results: bool = False, cursor: mysql.connector.cursor.MySQLCursor = None) -> tuple:
        """
        Executes an SQL query and returns the results (if any).

        Args:
            query: The SQL query to execute.
            values: The values to be inserted into the query (optional).
            print_output: Flag to print the formatted query before execution (default: False).
            print_results: Flag to print the query results after execution (default: False).
            cursor: The cursor object to use for query execution (default: self.csr).

        Returns:
            The results of the query as a tuple.
        """
        if cursor is None:
            cursor = self.csr

        results = ()
        try:
            if values:
                formatted_query = query % tuple(values)
                if print_output:
                    print(f"executing: {formatted_query}")
                    print('-' * 60)
                cursor.execute(query, values)
            else:
                if print_output:
                    print(f"executing: {query}")
                    print('-' * 60)
                cursor.execute(query)

            # Retrieve the results (if any)
            results = cursor.fetchall()

            if print_results:
                for row in results:
                    print(row)

        except mysql.connector.IntegrityError as err:
            # Handle the duplicate username error
            raise DuplicateValue("Duplicate username entered. Please choose a different username.")

        # except Exception as err:
        #     print(f"An error occurred: {err}")

        return results


class DuplicateValue(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'Duplicate Value Error: {self.message}'
    

def map_types(cls: Type) -> Type:
    """
    Maps the annotated field types to MySQL data types.

    Args:
        cls: The class to map the field types for.

    Returns:
        The modified class with mapped field types.
    """
    for field_name, field_type in cls.__annotations__.items():
        mysql_type = cls.type_mapping.get(field_type)
        if mysql_type is None:
            raise ValueError(f"Unsupported data type: {field_type} for field {field_name}")
        setattr(cls, field_name, field_type)  # Set the original field type
        setattr(cls, f"__mysql_{field_name}_type__", mysql_type)  # Add the MySQL data type attribute
    return cls


@map_types
@dataclass
class Table:
    """
    A base class representing a table in the database.

    Attributes:
        type_mapping: A dictionary mapping Python data types to MySQL data types.
    """

    type_mapping = {
        int: 'INT',
        str: 'VARCHAR(255)',
        float: 'DECIMAL(10,2)',
        bool: 'BOOL',
        datetime: 'DATETIME'
    }


    def insert(self, db_inst, print_output: bool = False) -> None:
        """
        Inserts a new record into the table.

        Args:
            db_inst: The instance of myDB class to execute the query.

        Returns:
            None.
        """
        columns = []
        values = []
        upsert = False
        # print(f'self.__dataclass_fields__.values(): {self.__dataclass_fields__.values()}')
        for field in self.__dataclass_fields__.values():
            column_name = field.name
            attr_value = getattr(self, column_name)
            # print(field.metadata.get('primary_key', False))
            if column_name == 'id' and self.id:
                # print(f'id passed to insert method - column_name: {column_name} attr_value: {attr_value}')
                upsert = True
                columns.append(column_name)
                values.append(str(attr_value))

            if not field.metadata.get('primary_key', False):
                columns.append(column_name)

            if column_name == 'salt':
                salt = bcrypt.gensalt()
                attr_value = salt.decode('utf-8')
                print(f'salt: {salt}')

            if field.metadata.get('hashed', False): 

                # Hash a string with the generated salt
                password = attr_value.encode('utf-8')  # Convert the password string to bytes
                print(f'salt: {salt}')
                print(f'password: {password}')
                attr_value = bcrypt.hashpw(password, salt).decode('utf-8')

            if isinstance(attr_value, str):  # Check if attribute value is a string
                attr_value = f"'{attr_value}'"

            if isinstance(attr_value, datetime):
                attr_value = attr_value.strftime('%Y-%m-%d %H:%M:%S')[:19]
                attr_value = f"STR_TO_DATE('{attr_value}', '%Y-%m-%d %H:%i:%s')"
            
            if not field.metadata.get('primary_key', False):
                values.append(str(attr_value))

        table_name = self.__class__.__name__.lower()
        if upsert:
            merge_string = [f'{column}=VALUES({column})' for column in columns]
            query = f"""
                INSERT INTO {table_name} 
                ({', '.join(columns)}) 
                VALUES ({', '.join(values)})
                ON DUPLICATE KEY UPDATE 
                {', '.join(merge_string)};
                """
        else:
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        # print(f'insert method: {query}')
        try:
            print
            db_inst(query, print_output=print_output)
            db_inst.cnx.commit()
        except mysql.connector.IntegrityError as err:
            # Handle the duplicate username error
            print("Duplicate username entered. Please choose a different username.")



    @classmethod
    def create_table(cls, db_inst, print_output=False) -> None:
        """
        Creates the table in the database.

        Args:
            db_inst: The instance of myDB class to execute the query.
            print_output: Flag to print the query before execution (default: False).

        Returns:
            None.
        """
        schema = []
        for field in cls.__dataclass_fields__.values():
            mysql_type = cls.type_mapping.get(field.type)
            if mysql_type is not None and not field.metadata.get('primary_key', False):
                attr_values = f'{field.name} {mysql_type}'
                if field.metadata.get('unique'):
                    attr_values += " UNIQUE"
                schema.append(attr_values)

        table_name = cls.__name__.lower()
        create_tbl = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT, {', '.join(schema)}, PRIMARY KEY (id));"

        db_inst(create_tbl, print_output=print_output)


    def read(self, db_inst, **kwargs):
        """
        Retrieves records from the table based on the given conditions.

        Args:
            db_inst: The instance of myDB class to execute the query.
            **kwargs: Optional keyword arguments representing conditions.

        Returns:
            A list of dictionary objects representing the retrieved records.
        """
        if 'where' in kwargs.keys(): 
            where_clause = f" WHERE {kwargs['where']}"
        elif kwargs:
            conditions = [f"{column} = '{value}'" for column, value in kwargs.items()]
            where_clause = " WHERE " + " AND ".join(conditions)
        else:
            where_clause = ""

        table_name = self.__class__.__name__.lower()
        query = f"SELECT * FROM {table_name}{where_clause}"
        print(query)
        try:
            results = db_inst(query, values = kwargs['values'])
        except KeyError as err:
            results = db_inst(query)
            print(err)

        columns = [field.name for field in self.__dataclass_fields__.values()]

        result_objects = []
        for row in results:
            row_dict = {}
            for column, value in zip(columns, row):
                field_type = self.__annotations__[column]
                if field_type == int:
                    value = int(value)
                elif field_type == bool:
                    value = bool(value)
                row_dict[column] = value
            dict_element = self.__class__(**row_dict)

            result_objects.append(dict_element)

        if len(result_objects) == 1:
            return dict_element

        return result_objects
