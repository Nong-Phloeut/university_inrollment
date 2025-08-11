from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL connection URL format with PyMySQL driver
DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/school_mgmt"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
