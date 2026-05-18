from pydantic import BaseModel
from typing import Optional


class  CategoryBase(BaseModel):
    name: str
    class Config:
        from_attributes = True


class CategoryCreate(CategoryBase):
    pass
    class Config:
        from_attributes = True

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True
    
class SuppliersBase(BaseModel):
    name: str
    contact: Optional[str] = None
    class Config:
        from_attributes = True

class SupplierCreate(SuppliersBase):
    pass
    class Config:
        from_attributes = True

class SupplierResponse(SuppliersBase):
    id: int
    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    quantity: int
    price: float
    category_id: int
    supplier_id: int
    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass
    class Config:
        from_attributes = True

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
