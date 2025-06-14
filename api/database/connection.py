from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Para banco em memória:
DATABASE_URL = "sqlite:///:memory:"
# Para banco em arquivo (descomente se preferir persistir):
# DATABASE_URL = "sqlite:///./cats.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necessário para SQLite com múltiplas threads
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para ser usada em rotas FastAPI, se quiser (exemplo):
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
