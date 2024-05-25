from datetime import timedelta
from typing import List
from fastapi import APIRouter, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.db import conn
from passlib.context import CryptContext
from models.db_p import products, user
from modelo.m_pro import producto 
from modelo.m_user import Token, Users, Login
from modelo.token import create_access_token
import json

product = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@product.get("/products",response_model=List[producto])  
def getproduct():
    product = conn.execute(products.select()).fetchall()
    return product

@product.post("/products",response_model=producto)  
def getnew(p: producto):
    new_products = {"name":p.name,"price":p.price,"stock":p.stock,"category_id":p.category_id}
    result = conn.execute(products.insert().values(new_products))
    conn.commit()
    return {**p.dict(), "id": result}


@product.get("/products/{id}",response_model=producto)  
def index(id:str):
    product = conn.execute(products.select().where(products.c.id == id)).first()
    if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
    return product

@product.delete("/products/{id}")  
def delete(id : str):
    product = conn.execute(products.delete().where(products.c.id == id))
    if product.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
    conn.commit()
    raise HTTPException(status_code=200, detail="Product delete")


@product.put("/products/{id}",response_model=producto)  
def index(id:str, p: producto):
    new_products = {"name":p.name,"price":p.price,"stock":p.stock,"category_id":p.category_id}
    result = conn.execute(products.update().values(new_products).where(products.c.id == id))
    conn.commit()
    update  = conn.execute(products.select().where(products.c.id == id)).first()
    return  update

@product.post("/usuario",response_model=Users)  
def get_user(users:Users):
    existe = conn.execute(user.select().where(user.c.username == users.username)).first()
    if existe:
      return JSONResponse("usuario ya se encuentra en uso")
  
    new_users = {"username":users.username}
    new_users["password"] = pwd_context.hash(users.password.encode("utf-8"))
    result = conn.execute(user.insert().values(new_users)) 
    query = conn.execute(user.select().where(user.c.id == result.lastrowid)).first()
    conn.commit()
    return query

@product.post("/usuario/login",response_model=Login)  
def get_user(users:Login): 
    
     user_db = conn.execute(user.select().where(user.c.username == users.username)).first()
        
     if not user_db or not pwd_context.verify(users.password, user_db.password):
        return JSONResponse("Incorrect username or password")
        raise HTTPException(409,"Incorrect username or password") 
     
     access_token = create_access_token(
        data={"sub": users.username}
     )
     token = {"access_token":access_token, "token_type":"bearer"}
     return JSONResponse(token)

    #raise HTTPException(status_code=200, detail="login")


