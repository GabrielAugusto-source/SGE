from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import auth
from . import crud, models, schemas
from .database import get_db, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SGE - Sistema de Gerenciamento de Estoque", version="1.0.0")


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(user_data: schemas.UserCreate, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if not user or not auth.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Nome ou Senha incorretos")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/setup-user")
def setup_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"message": "Usuário criado com sucesso"}



@app.delete("/categories/all")
def delete_all_categories(db: Session = Depends(get_db)):
    crud.delete_all_categories(db=db)
    return {"detail": "Todas as categorias foram excluídas!"}

@app.post("/categories/", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=list[schemas.CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db=db)

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    success = crud.delete_category(db=db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted successfully"}


@app.post("/suppliers/", response_model=schemas.SupplierResponse)
def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    # Ajustado para 'contact' para bater com o schema
    db_supplier = models.Supplier(name=supplier.name, contact=supplier.contact)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@app.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Usando a função do crud com underline (ajuste no crud.py se necessário)
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=list[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db=db)

@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    # Note que no crud.py o argumento chama-se product_data
    db_product = crud.update_product(db=db, product_id=product_id, product_data=product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db=db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/suppliers/", response_model=list[schemas.SupplierResponse])
def read_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db=db)
