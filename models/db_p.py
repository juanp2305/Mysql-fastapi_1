from pydantic import BaseModel
from sqlalchemy import Integer, String, Table, Column, true, ForeignKey
from config.db import meta, engine
category = Table(
    "category",
    meta,
    Column("id", Integer, primary_key=true),
    Column("name", String(255)),
    #relationship("product", backref="category")
)
products = Table(
    "product",
    meta,
    Column("id", Integer, primary_key=true),
    Column("name", String(255)),
    Column("price", Integer),
    Column("stock", Integer),
    Column("category_id", Integer, ForeignKey("category.id"),onupdate="CASCADE"),
)

user = Table(
    "user",
    meta,
    Column("id", Integer, primary_key=true),
    Column("username", String(255)),
    Column("password", String(255)),
    #relationship("product", backref="category")
)
meta.create_all(engine)
