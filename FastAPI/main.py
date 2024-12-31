# main file for FastAPI
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware #CORS auto defends against cross origin requests

app = FastAPI()

# a port or different app is allowed to call FastAPI only if it is running from the following list
origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

# create pydantic base model for the transaction, validates request from React app
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str


class TransactionModel(TransactionBase):
    id: int

    class Config:
        orm_mode = True

# create database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dependency injection for the database
db_dependency = Annotated[Session, Depends(get_db)]

#creating db and create tables and columns when FastAPI application is created
models.Base.metadata.create_all(bind=engine)

@app.post("/transactions/", response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    db_transaction = models.Transaction(amount=transaction.amount, category=transaction.category, description=transaction.description, is_income=transaction.is_income, date=transaction.date)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

