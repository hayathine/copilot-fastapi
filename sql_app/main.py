from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import sessionLocal, engine


models.Base.metadata.create_all(bind=engine) # データベースのテーブルを作成する

app = FastAPI()

origins = [
    "http://localhost:5173/todo",
    "http://localhost:5173",
    "http://localhosts"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 全てのHTTPメソッドを許可する
    allow_headers=["*"], # 全てのHTTPヘッダーを許可する
)

# Dependency
def get_db():
    db = sessionLocal()
    try:
        yield db # yieldは、関数を一時停止して、値を返すことができる
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User) # ユーザーを作成するエンドポイント
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user: # ユーザーが存在する場合
        raise HTTPException(status_code=400, detail="Email already registered") # 400エラーを返す
    return crud.create_user(db=db, user=user) # ユーザーを作成する

@app.get("/users/", response_model=list[schemas.User]) # ユーザーを全て取得するエンドポイント
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users # ユーザーを返す

@app.get("/users/{user_id}", response_model=schemas.User) # ユーザーIDからユーザーを取得するエンドポイント
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None: # ユーザーが存在しない場合
        raise HTTPException(status_code=404, detail="User not found") # 404エラーを返す
    return db_user # ユーザーを返す

@app.post("/users/{user_id}/items/", response_model=schemas.Item) # ユーザーのアイテムを作成するエンドポイント
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=list[schemas.Item]) # アイテムを全て取得するエンドポイント
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
