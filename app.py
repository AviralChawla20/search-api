from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List


# Replace these with your actual database connection details
DATABASE_URL = "mysql+mysqlconnector://sql12647981:XM51KVKzDA@sql12.freemysqlhosting.net:3306/sql12647981"


Base = declarative_base()


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    teamname = Column(String, index=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


app = FastAPI()

# Enable CORS for all origins (you might want to restrict this in a production environment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API endpoint for search
@app.get("/search/{query}", response_model=List[str])
def search(query: str, db: Session = Depends(get_db)):
    teams_result = (
        db.query(Team.teamname).filter(Team.teamname.ilike(f"%{query}%")).all()
    )

    users_result = db.query(User.name).filter(User.name.ilike(f"%{query}%")).all()

    # Combine and return the results
    result = [team[0] for team in teams_result] + [user[0] for user in users_result]
    return result


if __name__ == "__main__":
    import uvicorn

    # Run the application using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
