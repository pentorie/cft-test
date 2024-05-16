from datetime import date
import uvicorn
from fastapi import FastAPI, Security, Response, status
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from sqlalchemy import Column, Integer, Numeric, Date, String, create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet


# Настройка локальной базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Хеши для шифрования пароля и токена
SECRET_KEY = "XvYvP_c4gBDLCLbjgz6Hc47ND_BcoMYt3Cz5pAKx1qQ="
FERNET = Fernet(SECRET_KEY)
access_security = JwtAccessBearer(secret_key="secret_token_key", auto_error=True)


# Базовая моделька для работников
class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    password = Column(String, index=True)
    salary = Column(Numeric, index=True)
    raisedate = Column(Date, index=True)


Base.metadata.create_all(bind=engine)

app = FastAPI()


# Создание пользователя
@app.post("/register")
async def create_user(login: str, password: str, salary: float, raisedate: date):
    db = SessionLocal()
    encpass = FERNET.encrypt(password.encode()).decode()
    client = Worker(login=login, password=encpass, salary=salary, raisedate=raisedate)
    db.add(client)
    db.commit()
    db.refresh(client)
    return {"code": 200, "message": "UserCreated"}


# Авторизация
# Изначально реализовывал сохранением JWT-токена в куки, но потом подумал что Bearer для заголовков будет логичнее для отладки
@app.post("/login")
async def login(login: str, password: str, response: Response):
    db = SessionLocal()
    encpass = FERNET.encrypt(password.encode()).decode()
    res = db.query(Worker).filter(Worker.login == login).first()
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "UserNotFound"}
    else:
        stored_encpass = res.password
        decpass = FERNET.decrypt(stored_encpass.encode()).decode()
        if decpass == password:
            user_data = {"id": res.id, "login": res.login}
            access_token = access_security.create_access_token(subject=user_data)
            return {"token": access_token}
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "InvalidPassword"}


# Проверка зарплаты и даты следующего повышения работника. Работает получением информации из токена
@app.get("/salaryinfo")
async def salary_info(credentials: JwtAuthorizationCredentials = Security(access_security)):
    db = SessionLocal()
    res = db.query(Worker).filter(Worker.id == credentials["id"]).first()
    if res is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "TokenRequired"}
    else:
        return {"salary": res.salary, "raisedate": res.raisedate}


if __name__ == "__main__":
    uvicorn.run("main:app", port=3550)
