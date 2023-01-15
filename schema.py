from pydantic import BaseModel, Json
from typing import List, Union, Dict


class Product(BaseModel):
    name:str
    sku:str
    category:str
    price:Dict

    class Config:
        orm_mode = True

        

