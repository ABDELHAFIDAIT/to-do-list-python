import os
from dotenv import load_dotenv
from sqlalchemy import *
load_dotenv()

# import .env variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# create an engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

metadata = MetaData()

# create Tables
tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("description", Text, nullable=False),
    Column("priority", Enum("Low", "Medium", "High", name="enum_priority")),
    Column("status", Enum("Doing", "Done", name="enum_status"))
)

# add the Tasks Table to DB
try :
    metadata.create_all(engine)
except Exception as e :
    print("Error :\n", e)