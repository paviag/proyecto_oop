from __future__ import annotations
from enum import Enum
from datetime import date
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, Text, create_engine, select
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Item():
    def __init__(
        self,
        product_id: str,
        quantity: int,
        color: str,
        size: str,
    ) -> None:
        self.product_id = product_id
        self.quantity = quantity
        self.color = color
        self.size = size


class OrderStatus(Enum):
    PENDING = 'Por Aprobar'
    APPROVED = 'Aprobado/En Proceso de Envío'
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
    
    def __init__(
        self,
        order_id: str,
        total: float,
        buyer_name: str,
        buyer_email: str,
        buyer_phone: str,
        ship_city: str,
        ship_department: str,
        ship_address: str,
        ship_zipcode: str,
    ) -> None:
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
        pass
    

class OrderItem(Order, Item):
    __tablename__ = 'OrderItems'

    order_id = Column(ForeignKey('Orders.order_id'), primary_key=True)
    product_id = Column(ForeignKey('Products.product_id'))
    quantity = Column(Integer)
    color = Column(Text)
    size = Column(Text)

    product = relationship('Product')
    
    def __init__(
        self,
        order_id : str,
        product_id : str,
        quantity : int,
        color : str,
        size : str,
    ) -> None:
        self.order_id = order_id
        Item.__init__(
            self,
            product_id,
            quantity,
            color,
            size,
        )


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
    availability = Column(Boolean)

    def delete_product(self) -> None:
        pass
        
    def update(self) -> None:
        pass


class Cart():
    cart_items: list[CartItem] = []
    
    def __init__(self) -> None:
        self.cart_items = []
    
    @property
    def cart_total(self) -> float:
        return sum([item.item_total for item in self.cart_items])
    
    @property
    def total_quantity(self) -> int:
        return sum([item.quantity for item in self.cart_items])
    
    def add_item(self, item: CartItem) -> None:
        pass
        
    def remove_item(self, item: CartItem) -> None:
        pass
    
    def place_order(self) -> None:
        pass
    
   
class CartItem(Item):
    @property
    def item_total(self) -> float:
        pass
     

def get_session() -> sessionmaker:
    engine = create_engine('sqlite:///shop.db')
    Session = sessionmaker(bind=engine)
    return Session()

def get_available_products():
    session = get_session()
    query = session.query(Product).filter(Product.availability == 'True').all()
    return query