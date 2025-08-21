from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship,sessionmaker
from app.core.database import Base

#building tables that will be used in the database

class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String, unique=True, nullable=False)
    username = Column("username", String)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, email, username, password, active, admin=False):
        self.email = email
        self.username = username
        self.password = password
        self.active = active
        self.admin = admin


class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id")) 
    status = Column("status", String) # result in pending, finished, canceled
    price = Column("price", Float)
    items = relationship("OrderItem", cascade="all, delete")

    def __init__(self, user_id, status="PENDING", price=0):
        self.user_id = user_id
        self.status = status
        self.price = price
    
    def calculate_price(self):
        self.price = sum(item.unit_price * item.quantity for item in self.items)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer) 
    flavor = Column("flavor", String, nullable=False)
    size = Column("size", String)
    unit_price = Column("unit_price", Float)
    order_id = Column("order_id", Integer, ForeignKey("orders.id"))    

    def __init__(self, quantity, flavor, size, unit_price, order_id):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order_id = order_id

