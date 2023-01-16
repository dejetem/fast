import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException, status,Request
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.encoders import jsonable_encoder
from typing import List
import sqlalchemy 
from fastapi.responses import JSONResponse



from models import Product as ModelProduct

from schema import Product as SchemaProduct




load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])



@app.get("/")
async def root():
    return {"message": "Hello World, please go to /docs to test the api with swagger doc or /redoc"}

   

#get all most recent product
# @app.get("/products/")
# async def get_products():
#     products = db.session.query(ModelProduct).order_by(sqlalchemy.desc(ModelProduct.id)).offset(0).limit(10).all()

#     return products

# filtered by category as a query parameter
# @app.get('/product/{product_category}',response_model=List[SchemaProduct])
# async def get_products_by_category(product_category:str):
#     product = db.session.query(ModelProduct).filter(ModelProduct.category==product_category).order_by(sqlalchemy.desc(ModelProduct.id)).offset(0).limit(10).all()
#     return product

# filtered by  category and price less_than the original price as a query parameter
@app.get('/products',response_model=List[SchemaProduct])
async def get_products_by_price_and_category(product_price:int, product_category:str):
    print("product_price_original", product_price, product_category)
    product = db.session.query(ModelProduct).filter(ModelProduct.category==product_category, ModelProduct.price[("original")].cast(sqlalchemy.Integer) < product_price).order_by(sqlalchemy.desc(ModelProduct.id)).offset(0).limit(10).all()
    return product


#create a new product with or with discount
@app.post("/discounts", response_model=SchemaProduct)
async def add_product_with_discount_or_without(product:SchemaProduct):
    name = product.name
    sku = product.sku
    category = product.category
    my_price = product.price
 
    if my_price["original"] > 0:
        my_price["final"] = my_price["original"]
    if  "discount_percentage" not in my_price:
        my_price["discount_percentage"] = None
    if my_price["discount_percentage"] is not None:
        discount_percentage = my_price["discount_percentage"]
        new_discount = 100 - int(discount_percentage.replace('%', ''))
        print(new_discount)
        if my_price["original"] > 0:
            my_price["final"] = new_discount /100 * my_price["original"]



       
    
    db_product = ModelProduct(name=name, sku=sku, category=category, price=jsonable_encoder(my_price))
    db.session.add(db_product)
    db.session.commit()
    db.session.refresh(db_product)
    return db_product

# #create a new product
# @app.post("/add-product/", response_model=SchemaProduct)
# async def add_product(product:SchemaProduct):
#     name = product.name
#     sku = product.sku
#     category = product.category
#     my_price = product.price
#     discount_percentage = my_price["discount_percentage"]
#     new_discount = 100 - int(discount_percentage.replace('%', '')) 
 
#     if my_price["original"] > 0:
#         my_price["final"] = new_discount /100 * my_price["original"]
#     if my_price["original"] > 0 and new_discount == 0:
#         my_price["final"] = my_price["original"]

        
    
#     # original = price["original"]
#     # currency = price["currency"]
#     # new_discount = int(discount_percentage.replace('%', ''))
#     # print(new_discount)
#     db_product = ModelProduct(name=name, sku=sku, category=category, price=jsonable_encoder(my_price))
#     db.session.add(db_product)
#     db.session.commit()
#     db.session.refresh(db_product)
#     return db_product


