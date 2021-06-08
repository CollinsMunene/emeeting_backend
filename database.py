'''
/**
 * @author Collins Munene

 * @email hillarycollins@protonmail.com

 * @create date 2021-06-8 1:00:00
 * 
 * (c) Collins.
 */
'''
 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases
import os

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/restapi"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,echo=True
# )
# engine = create_engine(DATABASE_URL,echo = True)


# DATABASE_URL = os.environ.get('DATABASE_URL')


# database = databases.Database(DATABASE_URL)


# engine = create_engine(
#     DATABASE_URL, pool_size=3, max_overflow=0
# )

engine = create_engine("mysql+mysqlconnector://root@localhost:3306/all_meetings",echo = True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()