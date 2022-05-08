from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any, cast

import justpy as jp
from sqlalchemy import (Column, Float, ForeignKey, Integer, Text,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker

Base = declarative_base()
metadata = Base.metadata


class Category(Enum):
    UPPER_BODY = 'Prendas Superiores'
    PANTS = 'Pantalones'
    SKIRTS = 'Faldas'
    ACCESSORIES = 'Accesorios'
    MAKEUP = 'Maquillaje'


class Product(Base):
    __tablename__ = 'Products'

    product_id = Column(Text, primary_key=True)
    name = Column(Text)
    price = Column(Float)
    category = Column(Text)
    description = Column(Text)
    images = Column(Text)
    colors = Column(Text)
    sizes = Column(Text)
    available_units = Column(Integer)

    def delete_product(self) -> None:
        """Deletes a product from database."""
        ...
        
    def update_product(self) -> None:
        """Modifies a product's attributes, and subsequently, its row in
        the database."""
        ...


class Item():
    def __init__(self, product_id: str, quantity: int,
                 color: str, size: str) -> None:
        self.product_id = product_id
        self.quantity = quantity
        self.color = color
        self.size = size
    
    @property
    def related_product(self) -> Product | None:
        """Returns the item's corresponding product or None if the product 
        is not found in the database."""
        
        return get_from_db(Product, self.product_id)


class OrderStatus(Enum):
    PENDING = 'Por Aprobar'
    APPROVED = 'En Proceso de Envío'
    DENIED = 'Denegado'
    DELIVERED = 'Finalizado'


class Order(Base):
    __tablename__ = 'Orders'

    order_id = Column(Text, primary_key=True)
    total = Column(Float)
    buyer_name = Column(Text)
    buyer_email = Column(Text)
    buyer_phone = Column(Text)
    ship_city = Column(Text)
    ship_department = Column(Text)
    ship_address = Column(Text)
    ship_zipcode = Column(Text)
    date = Column(Text)
    status = Column(Text)
    
    def __init__(self, order_id: str, total: float, buyer_name: str,
                 buyer_email: str, buyer_phone: str, ship_city: str,
                 ship_department: str, ship_address: str,
                 ship_zipcode: str) -> None:
        self.order_id = order_id
        self.total = total
        self.buyer_phone = buyer_phone
        self.buyer_name = buyer_name
        self.buyer_email = buyer_email
        self.ship_city = ship_city
        self.ship_department = ship_department
        self.ship_address = ship_address
        self.ship_zipcode = ship_zipcode
        self.date = str(date.today())
        self.status = OrderStatus.PENDING.value
        
    def update_status(self, new_status: OrderStatus) -> None:
        """Modifies the status of an order or deletes it from database if its
        new status is DELIVERED.
        
        Parameters:
        new_status (str): New status to assign to the order.
        """
        
        # TODO (hopefully): change so that modification and deletion can 
        # happen from the get-go without fetching again from database
        session = get_session()
        db_object = session.get(Order, self.order_id)
        if new_status == OrderStatus.DELIVERED:
            session.delete(db_object)
        else:
            db_object.status = new_status.value
        session.commit()
        

class OrderItem(Base, Item):
    __tablename__ = 'OrderItems'

    order_id = Column(ForeignKey('Orders.order_id'))#, ondelete='CASCADE'))
    product_id = Column(ForeignKey('Products.product_id'))
    quantity = Column(Integer)
    color = Column(Text)
    size = Column(Text)

    product = relationship('Product')
    order = relationship('Order', backref=backref('orderitems', cascade='all,delete'))
    
    __mapper_args__ = {
        'primary_key':[order_id, product_id, quantity, color, size]
    }
    
    def __init__(self, order_id: str, product_id: str, quantity: int,
                 color: str, size: str) -> None:
        self.order_id = order_id
        Item.__init__(self, product_id, quantity, color, size)


class CartItem(Item):
    @property
    def item_total(self) -> float:
        """Returns item total."""
        
        product = super().related_product
        return product.price*self.quantity
    
    def __eq__(self, other: Any) -> bool:
        """Returns True if both items' attributes, save for quantity, 
        have the same values.
        
        Parameters:
        other (Any): Other Cart Item to compare to.
        """
        
        other = cast(CartItem, other)
        return all([self.product_id==other.product_id,
                    self.color==other.color,
                    self.size==other.size])
        
    def change_quantity(self, amount: int) -> None:
        """Changes item quantity by given amount.
        
        Parameters:
        amount (int): Number to add to item quantity.
        """
        
        new_quantity = self.quantity+amount
        if (self.related_product.available_units-new_quantity>0 and new_quantity>0):
            self.quantity = new_quantity
        else:
            raise Exception('No hay suficientes unidades disponibles.')

     
class Cart():
    def __init__(self) -> None:
        self.cart_items = []
    
    @property
    def cart_total(self) -> float:
        """Returns cart total."""
        
        if len(self.cart_items) > 0:
            return sum([item.item_total for item in self.cart_items])
        else:
            return 0
    
    @property
    def total_quantity(self) -> int:
        """Returns total number of items in cart."""
        
        if len(self.cart_items) > 0:
            return sum([item.quantity for item in self.cart_items])
        else:
            return 0
    
    def add_item(self, product_id: str, quantity: int, 
                 color: str, size: str) -> None:
        """Adds item to cart.
        
        If the resulting item quantity does not surpass the related product's
        available units, it adds a new item to add to cart. If the item
        items.
        
        Parameters:
        product_id (str): ID of the product that the item to add corresponds
        to.
        quantity (int): Quantity of item to add.
        color (str): Color of item to add.
        size (str): Size of item to add.
        """
        
        new_item = CartItem(product_id, quantity, color, size)
        if quantity > 0:
            # Checks if item already exists in cart to add its new quantity
            # to the quantity of the existing item or else append new item to
            # cart items
            for item_in_cart in self.cart_items:
                if new_item == item_in_cart:
                    try:
                        item_in_cart.change_quantity(new_item.quantity)
                        break
                    except:
                        raise Exception('No hay suficientes unidades '\
                                        'disponibles.')
            else:
                # Checks if there are enough available units
                if new_item.related_product.available_units > new_item.quantity:
                    self.cart_items.append(new_item)
                else:
                    raise Exception('No hay suficientes unidades '\
                                    'disponibles.')
        
    def remove_item(self, item: CartItem) -> None:
        """Removes an item from cart items.
        
        Parameters:
        item (CartItem): Cart item to remove.
        """
        
        self.cart_items.remove(item)
    
    def place_order(self, new_order_id: str, buyer_info: dict[str, str]) -> None:
        """Creates a new order. 
        
        Parameters:
        new_order_id (str): ID of order to be created.
        buyer_info (dict): Buyer information.
        """
        
        if row_count(Order) > 10**9:
            # Limit of orders in database has been reached
            raise Exception('Límite de órdenes alcanzado.')
        else:
            # Creates order with given information and adds to database
            new_order_id = get_new_id(Order.order_id)
            new_order = Order(
                order_id=new_order_id,
                total=self.cart_total,
                buyer_name=buyer_info['name'],
                buyer_email=buyer_info['email'],
                buyer_phone=buyer_info['phone'],
                ship_city=buyer_info['city'],
                ship_department=buyer_info['department'],
                ship_address=buyer_info['address'],
                ship_zipcode=buyer_info['zipcode'],
            )
            for item in self.cart_items:
                # Adds cart items to new order as orderitems
                new_order_item = OrderItem(
                    order_id=new_order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    color=item.color,
                    size=item.size,
                )
                new_order.orderitems.append(new_order_item)
            # Adds new order alongside its orderitems to database
            add_to_db(new_order)
            self.cart_items.clear()


class Section():
    def __init__(self, name: str, link) -> None:
        self.name = name
        self.link = link


class TabsPills(jp.Div):
    """Modified version of class TabPills referenced in JustPy docs. 
    
    Allows greater personalization for styling.
    """
    
    item_classes = 'flex-shrink m-1'
    item_classes_selected = 'flex-shrink m-1'
    wrapper_style = 'display: flex; flex-wrap: wrap; width: 100%;'\
                    'height: 100%;  align-items: center;'\
                    'justify-content: center; background-color: #fff;'\
                    'font-family: \'Poppins\', sans-serif;'

    def __init__(self, **kwargs):
        self.tabs = []  # list of {'id': id, 'label': label, 'content': content}
        self.value = None  # The value of the tabs component is the id of the selected tab
        self.content_height = 600
        self.last_rendered_value = None
        self.text_color = 'black'
        self.hover_bg = 'gray-100'
        self.selected_text_color = 'pink-400'
        self.tab_list_bg = 'white'
        self.border = ''
        
        super().__init__(**kwargs)

        self.tab_label_classes = f'cursor-pointer inline-block rounded-lg m-3 py-1 px-3 text-{self.text_color} font-semibold hover:bg-{self.hover_bg}'
        self.tab_label_classes_selected = f'cursor-pointer inline-block rounded-lg m-3 py-1 px-3 text-{self.selected_text_color} font-semibold'
        self.tab_list = jp.Ul(classes=f'flex overflow-x-auto text-center text-md bg-{self.tab_list_bg} items-center justify-between px-8 {self.border}', a=self)
        self.content_div = jp.Div(a=self)
        self.delete_list = []


    def __setattr__(self, key, value):
        if key == 'value':
            try:
                self.previous_value = self.value
            except:
                pass
        self.__dict__[key] = value

    def add_tab(self, id, label, content):
        self.tabs.append({'id': id, 'label': label, 'content': content})
        if not self.value:
            self.value = id

    def get_tab_by_id(self, id):
        for tab in self.tabs:
            if tab['id'] == id:
                return tab
        return None

    def set_content_div(self, tab):
        self.content_div.add(tab['content'])
        self.content_div.set_classes('overflow-auto relative overflow-hidden')
        self.content_div.style = f'height: {self.content_height}px;'
    
    def model_update(self):
        val = self.model[0].data[self.model[1]]
        if self.get_tab_by_id(val):
            self.value = val

    def delete(self):
        for c in self.delete_list:
            c.delete_flag = True
            c.delete()
            c.needs_deletion = False

        if self.delete_flag:
            for tab in self.tabs:
                tab['content'].delete()
                tab['content'] = None
        super().delete()

    @staticmethod
    async def tab_click(self, msg):
        if self.tabs.value != self.tab_id:
            previous_tab = self.tabs.value
            self.tabs.value = self.tab_id
            if hasattr(self.tabs, 'model'):
                self.tabs.model[0].data[self.tabs.model[1]] = self.tabs.value
            # Run change if it exists
            if self.tabs.has_event_function('change'):
                msg.previous_tab = previous_tab
                msg.new_tab = self.tabs.value
                msg.id = self.tabs.id
                msg.value = self.tabs.value
                msg.class_name = self.tabs.__class__.__name__
                return await self.tabs.run_event_function('change', msg)
        else:
            return True  # No need to update page

    def convert_object_to_dict(self):
        if hasattr(self, 'model'):
            self.model_update()
        self.set_classes('flex flex-col')
        self.tab_list.delete_components()
        self.content_div.components = []
        for tab in self.tabs:
            if tab['id'] != self.value:
                tab_li = jp.Li(a=self.tab_list, classes=self.item_classes)
                li_item = jp.A(text=tab['label'], classes=self.tab_label_classes, a=tab_li, delete_flag=False)
                self.delete_list.append(li_item)
            else:
                tab_li = jp.Li(a=self.tab_list, classes=self.item_classes_selected)
                li_item = jp.A(text=tab['label'], classes=self.tab_label_classes_selected, a=tab_li, delete_flag=False)
                self.delete_list.append(li_item)
                self.set_content_div(tab)
            li_item.tab_id = tab['id']
            li_item.tabs = self
            li_item.on('click', self.tab_click)
        self.last_rendered_value = self.value
        d = super().convert_object_to_dict()

        return d


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
