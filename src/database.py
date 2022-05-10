from __future__ import annotations

from typing import Any

from sqlalchemy import Column, Integer, create_engine, func
from sqlalchemy.orm import sessionmaker

def get_session() -> sessionmaker:
    """Returns session to connect to the database."""
    engine = create_engine('sqlite:///shop.db')
    Session = sessionmaker(bind=engine)
    return Session()

def add_to_db(object: Any) -> None:
    """Adds an object to database.
    
    Parameter:
    object (Any): object which follows the schema for a database
    table.
    """
    session = get_session()
    session.add(object)
    session.commit()

def delete_from_db(table_class, key: str) -> None:
    """Deletes an object from a table in the database according to its 
    primary key.
    
    Parameters:
    table_class (class): Class that corresponds to a database table.
    key (str): Primary key of object to delete.
    """
    session = get_session()
    object = session.get(table_class, key)
    session.delete(object)
    session.commit()

def get_from_db(table_class, key: str) -> Any | None:
    """Fetches a row from a table in the database according to its 
    primary key. 
    
    Returns row if found and None if not found.
    
    Parameters:
    table_class (class): Class that corresponds to a database table.
    key (str): Primary key of the row to fetch.
    
    Returns:
    Any: Row fetched from database.
    """
    session = get_session()
    return session.get(table_class, key)

def get_table_objects(
        table_class: Product | Order | OrderItem,
        condition: bool | None = None,
    ) -> list[Product | Order | OrderItem]:
    """Returns a list of rows from a table. 
    
    If a condition is given, it returns only the rows that match said
    condition.
    
    Parameters:
    table_class (class): Class that corresponds to a database table.
    condition (bool): Criteria by which table rows will be filtered.
    """
    session = get_session()
    if condition is None:
        return session.query(table_class).all()
    else:
        return session.query(table_class).filter(condition).all()

def row_count(table_class) -> int:
    """Returns number of rows of a table in the database.
    
    Parameters:
    table_class (class): Class that corresponds to a database table.
    """
    session = get_session()
    return session.query(table_class).count()

def get_new_id(id_column: Column | str) -> str:
    """Returns ID for a new row in a database table.
    
    The ID generated is a six-character string that is made up of a number
    ranging from one to a million padded with zeroes on the left. This ID
    will not be occupied by any other row in the table.
    
    Parameters:
    id_column (str): Column of a database table that contains its ID.
    
    Returns:
    str: Corresponds to the ID that should be assigned to a new row.
    """
    session = get_session()
    # Gets the maximmum value among stored IDs if these were integers
    max_table_id = session.query(func.max(id_column.cast(Integer))).first()[0]
    if max_table_id != None:    # Checks if column has data
        if max_table_id < 10**9:
            # Assigns max ID value increased by one unit and fills spaces to 
            # the left with zeroes until resulting ID has a length of six
            return str(max_table_id+1).zfill(6)
        else:
            # Starts from ID 000001 until finding an ID that does not 
            # correspond to an already existing row in the given column
            new_id_number = 1
            repeated_id = id_column==str(new_id_number).zfill(6)
            while session.query(id_column).filter(repeated_id).first() is not None:
                new_id_number += 1
                repeated_id = id_column==str(new_id_number).zfill(6)
            return str(new_id_number).zfill(6)
    else:
        # Assigns starting ID value (000001)
        return '1'.zfill(6)
