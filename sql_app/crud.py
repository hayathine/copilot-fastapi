# CRUD操作を行うファイル

from sqlalchemy.orm import Session
from . import models, schemas

# ユーザーIDからユーザーを取得する関数
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# ユーザーのメールアドレスからユーザーを取得する関数
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# ユーザーを全て取得する関数
def get_users(db: Session, skip: int = 0, limit: int = 100): 
    return db.query(models.User).offset(skip).limit(limit).all()

# ユーザーを作成する関数
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password) # ユーザーを作成する
    db.add(db_user) # ユーザーを追加する
    db.commit() # データベースにコミットする
    db.refresh(db_user) # データベースからユーザーをリフレッシュする
    return db_user # ユーザーを返す

# アイテムを取得する関数
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# ユーザーのアイテムを作成する関数
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int): 
    db_item = models.Item(**item.dict(), owner_id=user_id) # アイテムを作成する
    db.add(db_item) # アイテムを追加する
    db.commit() # データベースにコミットする
    db.refresh(db_item) # データベースからアイテムをリフレッシュする
    return db_item # アイテムを返す