from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Caminho para o arquivo do banco de dados SQLite
SQLITE_FILE_PATH = "test.db"

# Cria a URL de conexão para o SQLite
DATABASE_URL = f"sqlite:///{SQLITE_FILE_PATH}"

# Cria o engine do banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria uma função para obter uma sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria a base para as classes do modelo
Base = declarative_base()